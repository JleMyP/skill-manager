from typing import List, Optional

from constance import config

from core.clients.github import GithubClient, GithubRepo

from ..models import (
    ImportedResourceRepo,
    Resource,
    ResourceType,
    TagValue,
)

__all__ = ['import_stars', 'create_resources', 'create_resource']


class GithubUserNameNotSpecifiedException(Exception):
    """Не указан пользователь для импорта."""


class GitResourceTypeNotExists(Exception):
    """Не существует типа для ресурсов гита."""


def import_stars(username: Optional[str] = None,
                 token: Optional[str] = None) -> List[ImportedResourceRepo]:
    """Скачивает и сохраняет звезды указанного или дефолтного пользователя.

    :param username: имя пользователя, чьи лайки качать.
                     Если не указано - берется константа GITHUB_DEFAULT_USER.
    :param token: персональный токен гитхаба.
                  Если не указано - берется константа GITHUB_TOKEN.
    :return: список моделей, сохраненных в базу.
    :raises GithubUsernameNotSpecifiedException: не указано имя пользователя и константа пуста.
    """
    if not username:
        username = config.GITHUB_DEFAULT_USER
    if not token:
        token = config.GITHUB_TOKEN
    if not username:
        raise GithubUserNameNotSpecifiedException

    client = GithubClient(token)
    data = client.get_starred(username)
    repos = save_imported_stars(data)
    return repos


def save_imported_stars(data: List[GithubRepo]) -> List[ImportedResourceRepo]:
    """Сохраняет звезданутые репозитории в базу.

    :param data: список репозиториев, которые сохранить.
    :return: список моделей, сохраненных в базу.
    """
    imported_resources = []

    for repo in data:
        ir, created = ImportedResourceRepo.objects.update_or_create(
            name=repo.full_name,
            defaults={
                'description': repo.description,
                'short_name': repo.name,
                'url': repo.url,
                'homepage': repo.homepage,
                'language': repo.language,
                'topics': repo.topics,
                'from_user': repo.from_user,
                'raw_data': repo.raw,
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
    if not token:
        token = config.GITHUB_TOKEN
    client = GithubClient(token=token)
    resources = [_create_resource(res, client) for res in qs]
    resources = [res for res in resources if res]
    return resources


def create_resource(repo: ImportedResourceRepo,
                    token: Optional[str] = None) -> Optional[Resource]:
    """Создает или возвращает текущий ресурс для репозитория.

    :param repo: импортированный ресурс (репозиторий).
    :param token: персональный токен гитхаба.
    :return: None, если импортированный ресурс в игноре, иначе - ресурс.
    :raises GitResourceTypeNotExists: не указан id типа ресурса или указанный id не существует.
    """
    if not token:
        token = config.GITHUB_TOKEN
    client = GithubClient(token=token)
    return _create_resource(repo, client)


def _create_resource(repo: ImportedResourceRepo,
                     client: GithubClient) -> Optional[Resource]:
    """Создает или возвращает текущий ресурс для репозитория.

    :param repo: импортированный ресурс (репозиторий).
    :param client: гитхабовый клиент.
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

    owner, repo = repo.name.split('/')
    readme = client.get_readme(owner, repo)

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
