"""
Работа с устройствами
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi
from firezone_api.models import Device


class Devices:

    def __init__(self):
        self._api = FirezoneApi()

    async def get_devices(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает список устройств
        """
        devices: list[Device] = await self._api.get_devices()
        answer = ""
        for i, device in enumerate(devices):
            answer += f"Устройство №{i+1}:"
            answer += f"\nИмя: {device.name}"
            if device.rx_bytes is not None:
                recieved_value, recieved_descr = self.format_bytes(device.rx_bytes)
                answer += f"\nПолучено: {recieved_value} {recieved_descr}"
            else:
                answer += f"\nПолучено: -"
            if device.tx_bytes is not None:
                sent_value, sent_descr = self.format_bytes(device.tx_bytes)
                answer += f"\nОтправлено: {sent_value} {sent_descr}"
            else:
                answer += f"\nОтправлено: -"
            answer += f"\nПоследнее рукопожатие: {device.latest_handshake}"
            answer += '\n\n'
        await callback_query.message.answer(answer)

    @staticmethod
    def format_bytes(size):
        """
        Приводит к читаемому виду байты
        """
        power = 2 ** 10
        n = 0
        power_labels = {0: '', 1: 'Kb', 2: 'Mb', 3: 'Gb', 4: 'Tb'}
        while size > power:
            size /= power
            n += 1
        return round(size, 2), power_labels[n]  # +'байт'
