"""
Работа с устройствами
"""
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from firezone_api import FirezoneApi
from firezone_api.models import Device
from telegram_bot.backend import prepare_configuration_qr_and_message
from telegram_bot.backend.db.actions import get_user_by_chat_id


class Devices:
    device_info_prefix = "device_info_"
    device_list_prefix = "get_devices"

    def __init__(self):
        self._api = FirezoneApi()

    async def get_devices(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Отображает список устройств
        """
        chat_id = callback_query.message.chat.id
        fz_user = await get_user_by_chat_id(chat_id=chat_id)
        fz_user_id = fz_user.fz_user_id
        devices: list[Device] = await self._api.get_devices(user_id=fz_user_id)
        answer = ""
        if len(devices) == 0:
            answer = "Еще нет устройств"
        for i, device in enumerate(devices):
            answer += f'{i + 1}) "{device.name}":'
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
        if len(devices) != 0:
            answer += "Посмотреть детали:"
        keyboard = InlineKeyboardMarkup()
        self._fill_buttons_for_list_devices(devices=devices, keyboard=keyboard)
        keyboard.add(InlineKeyboardButton("Добавить устройство",
                                          callback_data="/create_device"))
        await callback_query.message.answer(answer, reply_markup=keyboard)

    def _fill_buttons_for_list_devices(self, devices: list[Device], keyboard: InlineKeyboardMarkup):
        """Создает клавиатуру для списка устройств"""
        prefix = self.__class__.device_info_prefix
        row = []
        devices_number_in_row = 2
        for i, device in enumerate(devices):
            if len(row) == devices_number_in_row:
                if len(row) != 0:
                    keyboard.add(*row)
                row = []
            button_text = f'{i + 1}) "{device.name}"'
            row.append(InlineKeyboardButton(button_text,
                                            callback_data=f"/{prefix}{device.id}"))

        if len(row) != 0:
            keyboard.add(*row)


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
        chat_id = message.chat.id
        fz_user = await get_user_by_chat_id(chat_id=chat_id)
        fz_user_id = fz_user.fz_user_id
        device = await self._api.create_device(user_id=fz_user_id, device_name=message.text.strip())
        config_file, qr_file = prepare_configuration_qr_and_message(device=device)
        message_text = "Ваш конфигурационный файл"
        await wait_message.delete()
        await message.answer_photo(photo=qr_file, caption=message_text)
        await message.answer_document(document=config_file)

    async def device_info(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Получает детальную информацию по устройству
        """
        prefix = self.__class__.device_info_prefix
        device_id = callback_query.data.replace(prefix, '')
        device = await self._api.get_device(device_id=device_id)
        if device.rx_bytes is not None:
            recieved_value, recieved_descr = self._format_bytes(device.rx_bytes)
            recieved_data = f"{recieved_value} {recieved_descr}"
        else:
            recieved_data = f"-"
        if device.tx_bytes is not None:
            sent_value, sent_descr = self._format_bytes(device.tx_bytes)
            sent_data = f"{sent_value} {sent_descr}"
        else:
            sent_data = f""
        text_message = (f'Имя устройства: "{device.name}"\n'
                        f"Описание: {device.description}\n"
                        f"Эндпоинт: {device.endpoint}\n"
                        f"Получено: {recieved_data}\n"
                        f"Отправлено: {sent_data}\n"
                        f"DNS: {device.dns}\n")
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Назад",
                                          callback_data=f"/{self.__class__.device_list_prefix}"))
        await callback_query.message.answer(text_message, reply_markup=keyboard)

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
