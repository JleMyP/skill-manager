import json
import re
from typing import List

import requests

from ..models import ImportedResource


API_STARS_URL = 'https://api.github.com/users/{0}/starred'
LINK_REGEXP = re.compile(r'<[^>_]+[?&]page=(\d+)[^>]*>; rel="([^"]+)"')


class GithubApiException(Exception):
    pass


def get_data(user: str) -> List[dict]:
    data = []
    params = {
        'page': 1,
        'per_page': 100,
    }
    headers = {
        'accept': 'application/vnd.github.mercy-preview+json',
    }
    url = API_STARS_URL.format(user)
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
            })

        link_header = resp.headers['Link']
        link_dict = dict([pair[::-1] for pair in LINK_REGEXP.findall(link_header)])

        if 'last' not in link_dict:
            break

        params['page'] += 1

    return data


def save_imported_data(data: List[dict]) -> list[ImportedResourceRepo]:
    imported_resources = []

    for repo in data:
        ir, c = ImportedResourceRepo.objects.get_or_create(
            name=repo['full_name'],
            defaults={
                'description': repo['description'],
                'raw_data': json.dumps(repo),
            }
        )
        imported_resources.append(ir)

    return imported_resources
