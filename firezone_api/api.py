"""
Работа с Firezone API
Документация https://www.firezone.dev/docs/reference/rest-api/
"""
import aiohttp
import json

from telegram_bot import config
from firezone_api.models import User, Device
from firezone_api.generators import KeysGenerator


class FirezoneApi:
    def __init__(
        self, host: str = config.FZ_HOST, token: str = config.FZ_TOKEN
    ):
        self._host = host
        self._token = token
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self._keys_generator = KeysGenerator()

    async def get_users(self) -> list[User]:
        """
        Получает список пользователей
        """
        url = f"{self._host}/v0/users"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                users: dict = await response.json()
                users: list[dict] = users["data"]
                users: list[User] = [User(**user) for user in users]
                return users

    async def get_devices(self, user_id: str = None) -> list[Device]:
        """
        Получает список устройств

        Параметры:
        ----------
            user_id: str - Id Пользователя, если не указан - запрашиваются по всем пользователям
        """
        url = f"{self._host}/v0/devices"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                devices: dict = await response.json()
                devices: list[dict] = devices["data"]
                devices: list[Device] = [Device(**user) for user in devices]
                if user_id is not None:
                    # Фильтрация по user_id
                    devices: list[Device] = list(filter(lambda x: x.user_id == user_id, devices))
                return devices

    async def create_device(
        self, user_id: str, device_name: str, description: str = None
    ) -> Device:
        """
        Создает конфигурацию устройства
        """
        url = f"{self._host}/v0/devices"
        self._keys_generator.generate()
        params = {
            "device": {
                "description": description,
                "name": device_name,
                "preshared_key": self._keys_generator.preshared_key,
                "public_key": self._keys_generator.public_key,
                "user_id": user_id,
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self._headers, data=json.dumps(params)
            ) as response:
                device: dict = await response.json()
                device: dict = device["data"]
                return Device(
                    **device, private_key=self._keys_generator.private_key
                )
