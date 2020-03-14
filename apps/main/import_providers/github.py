import json
import re
from typing import List, TypedDict, Optional

import requests
from constance import config

from apps.main.models import (
    ImportedResourceRepo,
    Resource,
    ResourceType,
    TagValue,
)

__all__ = ['import_data']

API_STARS_URL = 'https://api.github.com/users/{0}/starred'
LINK_REGEXP = re.compile(r'<[^>_]+[?&]page=(\d+)[^>]*>; rel="([^"]+)"')


class GithubApiException(Exception):
    pass


class GithubUserNameNotSpecifiedException(Exception):
    pass


class GitRepo(TypedDict):
    name: str
    full_name: str
    url: str
    description: str
    from_user: str
    homepage: Optional[str]
    language: Optional[str]
    topics: List[str]


def get_data(username: str, start_page: int = 1, per_page: int = 100) -> List[GitRepo]:
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
        link_dict = dict([pair[::-1] for pair in LINK_REGEXP.findall(link_header)])

        if 'last' not in link_dict:
            break

        params['page'] += 1

    return data


def save_imported_data(data: List[GitRepo]) -> List[ImportedResourceRepo]:
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
                'raw_data': json.dumps(repo),
            }
        )
        if created:
            imported_resources.append(ir)

    return imported_resources


def import_data(username: str = None) -> List[ImportedResourceRepo]:
    if not username:
        username = config.GIT_DEFAULT_USER
    if not username:
        raise GithubUserNameNotSpecifiedException

    data = get_data(username)
    repo = save_imported_data(data)
    return repo


def create_resource_from_imported(repo: ImportedResourceRepo) -> Resource:
    if repo.is_ignored or hasattr(repo, 'resource'):
        return repo.resource

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
