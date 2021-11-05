import base64
import re
import sys
from typing import List, Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing import Dict as TypedDict

import requests
from constance import config

from ..models import (
    ImportedResourceRepo,
    Resource,
    ResourceType,
    TagValue,
)

__all__ = ['import_data', 'create_resources']

API_STARS_URL = 'https://api.github.com/users/{0}/starred'
LINK_REGEXP = re.compile(r'<[^>_]+[?&]page=(\d+)[^>]*>; rel="([^"]+)"')


class GithubApiException(Exception):
    """Неуспешный ответ апи гитхаба."""


class GithubUserNameNotSpecifiedException(Exception):
    """Не указан пользователь для импорта."""


class GitResourceTypeNotExists(Exception):
    """Не существует типа для ресурсов гита."""


class GitRepo(TypedDict):
    """Структура репозитория для упаковки ответа гитхаба."""

    name: str
    full_name: str
    url: str
    description: str
    from_user: str
    homepage: Optional[str]
    language: Optional[str]
    topics: List[str]


def create_session(token: Optional[str] = None) -> requests.Session:
    """Создает и настраивает сессию для апи.

    :param token: персональный токен гитхаба.
    """
    session = requests.Session()
    session.headers.update({
        'accept': 'application/vnd.github.mercy-preview+json',
    })
    if token:
        session.headers['authorization'] = f'token {token}'
    return session


def import_data(username: Optional[str] = None,
                token: Optional[str] = None) -> List[ImportedResourceRepo]:
    """Скачивает и сохраняет репозитории указанного или дефолтного пользователя.

    :param username: имя пользователя, чьи лайки качать.
                     Если не указано - берется константа GITHUB_DEFAULT_USER.
    :param token: персональный токен гитхаба.
                  Если не указано - берется константа GITHUB_TOKEN.
    :return: список моделей, сохраненных в базу.
    :raises GithubUserNameNotSpecifiedException: не указано имя пользователя и константа пуста.
    """
    if not username:
        username = config.GITHUB_DEFAULT_USER
    if not token:
        token = config.GITHUB_TOKEN
    if not username:
        raise GithubUserNameNotSpecifiedException

    data = get_data(username, token=token)
    repos = save_imported_data(data)
    return repos


def get_data(username: str, start_page: int = 1, per_page: int = 100,
             token: Optional[str] = None) -> List[GitRepo]:
    """Скачивает список лайкнутых репозиториев пользователя.

    :param username: имя пользователя, чьи лайки качать.
    :param token: персональный токен гитхаба.
    :param start_page: страница, с которой начать выгрузку. ну мало ли.
    :param per_page: кол-во элементов на странице при скачивании.
    :return: список репозиториев.
    :raises GithubApiException: апи гитхаба вернуло неуспешный ответ.
    """
    data = []
    params = {
        'page': start_page,
        'per_page': per_page,
    }
    session = create_session(token)
    url = API_STARS_URL.format(username)

    with session:
        while True:
            resp = session.get(url, params=params)
            resp_data = resp.json()
            if not resp.ok:
                raise GithubApiException(resp_data['message'], resp_data.get('errors'))

            for repo in resp_data:
                data.append({
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'url': repo['html_url'],
                    'description': repo['description'],
                    'homepage': repo['homepage'],
                    'language': repo['language'],
                    'topics': repo.get('topics', []),
                    'from_user': username,
                })

            link_header = resp.headers['Link']
            link_dict = {rel: page for page, rel in LINK_REGEXP.findall(link_header)}

            if 'last' not in link_dict:
                break

            params['page'] += 1

    return data


def save_imported_data(data: List[GitRepo]) -> List[ImportedResourceRepo]:
    """Сохраняет скачанные репозитории в базу.

    :param data: список репозиториев, которые сохранить.
    :return: список моделей, сохраненных в базу.
    """
    imported_resources = []

    for repo in data:
        ir, created = ImportedResourceRepo.objects.update_or_create(
            name=repo['full_name'],
            defaults={
                'description': repo['description'],
                'short_name': repo['name'],
                'url': repo['url'],
                'homepage': repo['homepage'],
                'language': repo['language'],
                'topics': repo['topics'],
                'from_user': repo['from_user'],
                'raw_data': repo,
            }
        )
        if created:
            imported_resources.append(ir)

    return imported_resources


def create_resources(token: Optional[str] = None) -> List[Resource]:
    """Создает ресурсы для всех репозиториев без такового и не в игноре.

    :param token: персональный токен гитхаба.
    :return: список созданных ресурсов.
    """
    qs = ImportedResourceRepo.objects.filter(
        is_ignored=False,
        resource=None,
    )
    session = create_session(token=token)
    resources = [create_resource(res, session=session) for res in qs]
    resources = [res for res in resources if res]
    return resources


def create_resource(repo: ImportedResourceRepo,
                    session: Optional[requests.Session] = None) -> Optional[Resource]:
    """Создает или возвращает текущий ресурс для репозитория.

    :param repo: импортированный ресурс (репозиторий).
    :param session: преднастроенная сессия.
    :return: None, если импортированный ресурс в игноре, иначе - ресурс.
    :raises GitResourceTypeNotExists: не указан id типа ресурса или указанный id не существует.
    """
    if repo.is_ignored:
        return
    exists = getattr(repo, 'resource', None)
    if exists:
        return exists

    rt_pk = config.GIT_IMPORT_RESOURCE_TYPE
    rt = ResourceType.objects.filter(pk=rt_pk).first()
    if not rt:
        raise GitResourceTypeNotExists

    if not session:
        session = create_session()

    owner, name = repo.name.split('/')
    # TODO: завернуть в rate limiter
    resp = session.get(f'https://api.github.com/repos/{owner}/{name}/readme')
    readme_data = resp.json()
    # TODO: учет кодировки из ответа
    readme = base64.decodebytes(readme_data['content'].encode()).decode()

    resource = Resource.objects.create(
        type=rt,
        imported_resource=repo,
        name=repo.name,
        description=repo.description,
        text=readme,
        link=repo.url,
    )

    tag_pk = config.GIT_IMPORT_TAG
    if tag_pk:
        tag_value = TagValue.objects.get(pk=tag_pk)
        resource.tag_values.add(tag_value)

    # TODO: git tags?
    return resource
