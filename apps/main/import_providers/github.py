import re
from typing import List

import requests

API_STARS_URL = 'https://api.github.com/users/{}/starred'
LINK_REGEXP = re.compile(r'<[^>_]+[?&]page=(\d+)[^>]*>; rel="([^"]+)"')


class GithubApiException(Exception):
    pass


def get_data(user: str) -> List[dict]:
    data = []
    params = {
        'page': 1,
        'per_page': 100
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
