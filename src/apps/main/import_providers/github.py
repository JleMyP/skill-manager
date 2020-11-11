import re
import sys

from typing import List, Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing import Dict as TypedDict

import requests
from constance import config

from apps.main.models import (
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


def import_data(username: str = None) -> List[ImportedResourceRepo]:
    """Скачивает и сохраняет репозитории указанного или дефолтного пользователя.

    :param username: имя пользователя, чьи лайки качать.
                     Если не указано - берется константа GIT_DEFAULT_USER.
    :return: список моделей, сохраненных в базу.
    :raises GithubUserNameNotSpecifiedException: не указано имя пользователя и константа пуста.
    """
    if not username:
        username = config.GIT_DEFAULT_USER
    if not username:
        raise GithubUserNameNotSpecifiedException

    data = get_data(username)
    repos = save_imported_data(data)
    return repos


def get_data(username: str, start_page: int = 1, per_page: int = 100) -> List[GitRepo]:
    """Скачивает список лайкнутых репозиториев пользователя.

    :param username: имя пользователя, чьи лайки качать.
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
    headers = {
        'accept': 'application/vnd.github.mercy-preview+json',
    }
    url = API_STARS_URL.format(username)
    while True:
        resp = requests.get(url, params=params, headers=headers)
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


def create_resources() -> List[Resource]:
    """Создает ресурсы для всех репозиториев без такового и не в игноре.

    :return: список созданных ресурсов.
    """
    qs = ImportedResourceRepo.objects.filter(
        is_ignored=False,
        resource=None,
    )
    resources = [res for res in map(create_resource, qs) if res]
    return resources


def create_resource(repo: ImportedResourceRepo) -> Optional[Resource]:
    """Создает или возвращает текущий ресурс для репозитория.

    :param repo: импортированный ресурс (репозиторий).
    :return: None, если импортированный ресурс в игноре, иначе - ресурс.
    """
    if repo.is_ignored:
        return
    exists = getattr(repo, 'resource', None)
    if exists:
        return exists

    rt_pk = config.GIT_IMPORT_RESOURCE_TYPE
    rt = ResourceType.objects.get(pk=rt_pk)
    resource = Resource.objects.create(
        type=rt,
        imported_resource=repo,
        name=repo.name,
        description=repo.description,
        link=repo.url,
    )

    tag_pk = config.GIT_IMPORT_TAG
    if tag_pk:
        tag_value = TagValue.objects.get(pk=tag_pk)
        resource.tag_values.add(tag_value)

    # TODO: git tags?
    return resource
