"""
Работа с Firezone API
Документация https://www.firezone.dev/docs/reference/rest-api/
"""
import aiohttp
import json

import config
from firezone_api.models import User, Device
from firezone_api.generators import KeysGenerator
from firezone_api.exceptions import CreateUserError, UserAlreadyExistsError


class FirezoneApi:
    def __init__(self, host: str = config.FZ_HOST, token: str = config.FZ_TOKEN):
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
                response_data: dict = await response.json()
                users: list[dict] = response_data["data"]
                users: list[User] = [User(**user) for user in users]
                return users

    async def get_user_by_id(self, user_id: str = None, email: str = None) -> User:
        """
        Получает информацию о пользователе

        Можно использовать либо "email" либо "user_id"
        """
        if user_id is None and email is None:
            raise ValueError('Необходимо использовать один из параметров "user_id" или "email"')
        _id = user_id
        if user_id is None:
            _id = email
        url = f"{self._host}/v0/users/{_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                response_data: dict = await response.json()
                user: dict = response_data["data"]
                user: User = User(**user)
                return user

    async def create_user(self, email: str, role: str = None, password: str = None) -> User:
        """
        Создает пользователя
        """
        url = f"{self._host}/v0/users"
        params = {"user": {"email": email}}
        if role:
            params.update(role=role)
        if password:
            params.update(password=password, password_confirmation=password)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self._headers, data=json.dumps(params)) as response:
                try:
                    response_data: dict = await response.json()
                    user: dict = response_data["data"]
                    return User(**user)
                except Exception as err:
                    message = f"Ошибка создания пользователя :: {type(err)} {err}"
                    try:
                        # Если пользователь уже существует
                        if response.status == 422:
                            email_list = (await response.json())['errors']['email']
                    except:
                        pass
                    else:
                        if "has already been taken" in email_list:
                            raise UserAlreadyExistsError
                    try:
                        message += (f"\nSTATUS CODE :: {response.status}\n"
                                    f"Ответ от сервера: {await response.text()}")
                    except:
                        pass
                    raise CreateUserError(message)

    async def delete_user(self, user_id: str = None, email: str = None) -> bool:
        """
        Удаляет пользователя

        Можно использовать либо "email" либо "user_id"
        """
        if user_id is None and email is None:
            raise ValueError('Необходимо использовать один из параметров "user_id" или "email"')
        _id = user_id
        if user_id is None:
            _id = email
        url = f"{self._host}/v0/users/{_id}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self._headers) as response:
                if not response.ok:
                    raise Exception(
                        f'Ошибка удаления пользователя id :: "{_id}"\n'
                        f"STATUS CODE :: {response.status}\n"
                        f"Ответ от сервера: {await response.text()}"
                    )
                return response.ok

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
                response_data: dict = await response.json()
                devices: list[dict] = response_data["data"]
                devices: list[Device] = [Device(**device) for device in devices]
                if user_id is not None:
                    # Фильтрация по user_id
                    devices = filter(lambda x: x.user_id == user_id, devices)
                    devices: list[Device] = list(devices)
                return devices

    async def get_device_by_id(self, device_id: str = None) -> Device:
        """
        Получает информацию об устройстве

        Параметры:
        ----------
            device_id: str - Id Устройства
        """
        url = f"{self._host}/v0/devices/{device_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                response_data: dict = await response.json()
                device: dict = response_data["data"]
                device: Device = Device(**device)
                return device

    async def create_device(self, user_id: str, device_name: str, description: str = None) -> Device:
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
            async with session.post(url, headers=self._headers, data=json.dumps(params)) as response:
                response_data: dict = await response.json()
                device: dict = response_data["data"]
                return Device(**device, private_key=self._keys_generator.private_key)

    async def delete_device(self, device_id: str) -> bool:
        """
        Удаляет конфигурацию устройства
        """
        url = f"{self._host}/v0/devices/{device_id}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self._headers) as response:
                if not response.ok:
                    raise Exception(
                        f'Ошибка удаления устройства id :: "{device_id}"\n'
                        f"STATUS CODE :: {response.status}\n"
                        f"Ответ от сервера: {await response.text()}"
                    )
                return response.ok
