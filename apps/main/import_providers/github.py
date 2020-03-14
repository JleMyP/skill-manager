import json
import re
from typing import List

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


def get_data(username: str) -> List[dict]:
    data = []
    params = {
        'page': 1,
        'per_page': 100,
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
                'topics': repo.get('topics'),
                'from_user': username,
            })

        link_header = resp.headers['Link']
        link_dict = dict([pair[::-1] for pair in LINK_REGEXP.findall(link_header)])

        if 'last' not in link_dict:
            break

        params['page'] += 1

    return data


def save_imported_data(data: List[dict]) -> List[ImportedResourceRepo]:
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
                'topics': repo['topics'] or [],
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
        return  # TODO: raise?

    data = get_data(username)
    imported_resources = save_imported_data(data)
    return imported_resources
