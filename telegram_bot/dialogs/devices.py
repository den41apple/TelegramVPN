"""
Работа с устройствами
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from firezone_api import FirezoneApi
from firezone_api.models import Device
from telegram_bot.backend import prepare_configuration_qr_and_message


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
            answer += f"Устройство №{i + 1}:"
            answer += f"\nИмя: {device.name}"
            if device.rx_bytes is not None:
                recieved_value, recieved_descr = self._format_bytes(device.rx_bytes)
                answer += f"\nПолучено: {recieved_value} {recieved_descr}"
            else:
                answer += f"\nПолучено: -"
            if device.tx_bytes is not None:
                sent_value, sent_descr = self._format_bytes(device.tx_bytes)
                answer += f"\nОтправлено: {sent_value} {sent_descr}"
            else:
                answer += f"\nОтправлено: -"
            answer += f"\nПоследнее рукопожатие: {device.latest_handshake}"
            answer += "\n\n"
        await callback_query.message.answer(answer)

    async def get_name_for_new_device(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Запрашивает имя для нового устройства
        """
        message_text = "Введите имя новой конфигурации:"
        await callback_query.message.answer(message_text)
        await state.set_state("enter_device_name")

    async def create_new_device(self, message: Message, state: FSMContext):
        """
        Получает имя нового устройства
        И создает конфигурацию
        """
        await state.set_state("*")
        wait_message = await message.answer("Создается конфигурация...")
        firezone_user_id = "6a00408c-f3bb-41fa-a37e-4f25c76ecb26"  # тестовый юзер
        device = await self._api.create_device(user_id=firezone_user_id, device_name=message.text.strip())
        config_file, qr_file = prepare_configuration_qr_and_message(device=device)
        message_text = "Ваш конфигурационный файл"
        await wait_message.delete()
        await message.answer_photo(photo=qr_file, caption=message_text)
        await message.answer_document(document=config_file)

    @staticmethod
    def _format_bytes(size):
        """
        Приводит к читаемому виду байты
        """
        power = 2**10
        n = 0
        power_labels = {0: "", 1: "Kb", 2: "Mb", 3: "Gb", 4: "Tb"}
        while size > power:
            size /= power
            n += 1
        return round(size, 2), power_labels[n]  # +'байт'
