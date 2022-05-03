import base64
import re
from dataclasses import dataclass
from typing import List, Optional

import requests

API_STARS_URL = 'https://api.github.com/users/{0}/starred'
API_README_URL = 'https://api.github.com/repos/{owner}/{repo}/readme'
LINK_REGEXP = re.compile(r'<[^>_]+[?&]page=(\d+)[^>]*>; rel="([^"]+)"')


class GithubApiException(Exception):
    """Неуспешный ответ апи гитхаба."""


@dataclass
class GithubRepo:
    """Структура репозитория для упаковки ответа гитхаба."""

    name: str
    full_name: str
    url: str
    description: str
    from_user: str
    homepage: Optional[str]
    language: Optional[str]
    topics: List[str]
    raw: dict


class GithubClient:
    """
    :param token: персональный токен гитхаба.
    """

    def __init__(self, token: Optional[str] = None) -> None:
        self.token = token
        self.session = self.create_session()

    def create_session(self) -> requests.Session:
        """Создает и настраивает сессию для апи.
        """
        session = requests.Session()
        session.headers.update({
            'accept': 'application/vnd.github.mercy-preview+json',
        })
        if self.token:
            session.headers['authorization'] = f'token {self.token}'
        return session

    def get_starred(self, username: str, start_page: int = 1,
                    per_page: int = 100) -> List[GithubRepo]:
        """Скачивает список лайкнутых репозиториев пользователя.

        :param username: имя пользователя, чьи лайки качать.
        :param start_page: страница, с которой начать выгрузку.
        :param per_page: кол-во элементов на странице при скачивании.
        :return: список репозиториев.
        :raises GithubApiException: апи гитхаба вернуло неуспешный ответ.
        """
        data: List[GithubRepo] = []
        params = {
            'page': start_page,
            'per_page': per_page,
        }
        url = API_STARS_URL.format(username)

        with self.session:
            while True:
                resp = self.session.get(url, params=params)
                resp_data = resp.json()
                if not resp.ok:
                    raise GithubApiException(resp_data['message'], resp_data.get('errors'))

                for repo in resp_data:
                    data.append(GithubRepo(
                        name=repo['name'],
                        full_name=repo['full_name'],
                        url=repo['html_url'],
                        description=repo['description'],
                        homepage=repo['homepage'],
                        language=repo['language'],
                        topics=repo.get('topics', []),
                        from_user=username,
                        raw=repo,
                    ))

                link_header = resp.headers['Link']
                link_dict = {rel: page for page, rel in LINK_REGEXP.findall(link_header)}

                if 'last' not in link_dict:
                    break

                params['page'] += 1

        return data

    def get_readme(self, owner: str, repo: str) -> str:
        with self.session:
            url = API_README_URL.format(owner=owner, repo=repo)
            resp = self.session.get(url)

        resp_data = resp.json()
        if not resp.ok:
            raise GithubApiException(resp_data['message'], resp_data.get('errors'))

        # TODO: учет кодировки из ответа
        readme = base64.decodebytes(resp_data['content'].encode()).decode()
        return readme
