"""
Работа с Firezone API
Документация https://www.firezone.dev/docs/reference/rest-api/
"""
import aiohttp

import config
from firezone_api.models import User


class FirezoneApi:

    def __init__(self, host: str = config.FZ_HOST, token: str = config.FZ_TOKEN):
        self._host = host
        self._token = token
        self._headers = {'Content-Type': 'application/json',
                         'Authorization': f'Bearer {token}'}

    async def get_users(self) -> list[User]:
        """
        Получает список пользователей
        """
        url = f"{self._host}/v0/users"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                users: list[dict] = await response.json()
                users = users['data']
                users = [User(**user) for user in users]
                return users
