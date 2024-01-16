"""
Работа с устройствами
"""
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery

from firezone_api import FirezoneApi
from firezone_api.models import Device
from telegram_bot.backend import prepare_configuration_qr_and_message
from telegram_bot.backend.db.actions import get_user_by_chat_id
from telegram_bot.backend.utils import extract_id_from_callback_data, escaping


class Devices:
    device_details_prefix = "device_details"
    device_confirm_delete_prefix = "device_confirm_delete"
    delete_device_prefix = "delete_device"
    device_list_prefix = "list_devices"

    def __init__(self):
        self._api = FirezoneApi()

    async def list_devices(self, callback_query: CallbackQuery, state: FSMContext, fz_user_id: str = None):
        """
        Отображает список устройств
        """
        await state.set_state("*")
        chat_id = callback_query.message.chat.id
        # Определим передан ли конкретный Id пользователя
        fz_user_id_from_data = extract_id_from_callback_data(callback_query)
        if fz_user_id is None:
            if fz_user_id_from_data is None:
                fz_user = await get_user_by_chat_id(chat_id=chat_id)
                fz_user_id = fz_user.fz_user_id
            else:
                fz_user_id = fz_user_id_from_data
        devices: list[Device] = await self._api.get_devices(user_id=fz_user_id)
        answer = "*Устройства:*\n\n"
        if len(devices) == 0:
            answer += "Еще нет устройств"
        for i, device in enumerate(devices):
            answer += f'{i + 1}) "{device.name}":'
            recieved_data = self._format_bytes(device.rx_bytes)
            answer += f"\nПолучено: {recieved_data}"
            sent_data = self._format_bytes(device.tx_bytes)
            answer += f"\nОтправлено: {sent_data}"
            answer += "\n\n"
        # if len(devices) != 0:
        #     answer += "Детали:"
        keyboard = InlineKeyboardMarkup()
        self._fill_buttons_for_list_devices(devices=devices, keyboard=keyboard)
        callback_data = "/create_device"
        if fz_user_id_from_data is not None:
            callback_data += f"_<id:{fz_user_id}>"
        keyboard.add(InlineKeyboardButton("Добавить устройство", callback_data=callback_data))
        answer = escaping(answer)
        await callback_query.message.answer(answer, reply_markup=keyboard, parse_mode="MarkdownV2")

    def _fill_buttons_for_list_devices(self, devices: list[Device], keyboard: InlineKeyboardMarkup):
        """Создает клавиатуру для списка устройств"""
        prefix = self.__class__.device_details_prefix
        row = []
        devices_number_in_row = 2
        for i, device in enumerate(devices):
            if len(row) == devices_number_in_row:
                if len(row) != 0:
                    keyboard.add(*row)
                row = []
            button_text = f'{i + 1}) "{device.name}"'
            row.append(InlineKeyboardButton(button_text, callback_data=f"/{prefix}_<id:{device.id}>"))

        if len(row) != 0:
            keyboard.add(*row)

    async def get_name_for_new_device(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Запрашивает имя для нового устройства
        """
        chat_id = callback_query.message.chat.id
        fz_user_id = extract_id_from_callback_data(callback_query)
        message_text = ""
        if fz_user_id is not None:
            # Если в режиме админа
            fz_user = await self._api.get_user_by_id(user_id=fz_user_id)
            # TODO: Отработать вариант с отсутствием пользователя
            message_text = f'Добавление устройства для пользователя "{fz_user.email}"\n\n'
        else:
            user = await get_user_by_chat_id(chat_id=chat_id)
            fz_user_id = user.fz_user_id
        message_text += "Введите имя новой конфигурации:"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Отмена", callback_data=f"/{self.__class__.device_list_prefix}"))
        await asyncio.gather(
            callback_query.message.answer(message_text, reply_markup=keyboard),
            state.update_data({"user_id": fz_user_id}),
        )
        await state.set_state("enter_device_name")

    async def create_new_device(self, message: Message, state: FSMContext):
        """
        Получает имя нового устройства
        И создает конфигурацию
        """
        data = await state.get_data()
        fz_user_id = data.pop("user_id")
        await state.update_data(data)
        await state.set_state("*")
        wait_message = await message.answer("Создается конфигурация...")
        device = await self._api.create_device(user_id=fz_user_id, device_name=message.text.strip())
        config_file, qr_file = prepare_configuration_qr_and_message(device=device)
        message_text = "QR код для сканирования"
        await wait_message.delete()
        await message.answer_photo(photo=qr_file, caption=message_text)
        message_text = "Конфигурация"
        await message.answer_document(document=config_file, caption=message_text)

    async def device_details(self, callback_query: CallbackQuery, state: FSMContext):
        """
        Получает детальную информацию по устройству
        """
        callback_data = callback_query.data
        device_id = extract_id_from_callback_data(callback_query)
        device = await self._api.get_device_by_id(device_id=device_id)
        text_message = self._create_device_details_message(device=device)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "Удалить", callback_data=f"/{self.__class__.device_confirm_delete_prefix}_<id:{device_id}>"
            )
        )
        keyboard.add(InlineKeyboardButton("Назад", callback_data=f"/{self.__class__.device_list_prefix}"))
        if "<edit>" in callback_data:
            return await callback_query.message.edit_text(text_message, reply_markup=keyboard, parse_mode="MarkdownV2")
        await callback_query.message.answer(text_message, reply_markup=keyboard, parse_mode="MarkdownV2")

    def _create_device_details_message(self, device: Device) -> str:
        """Формирует детальную информацию об устройстве"""
        recieved_data = self._format_bytes(device.rx_bytes)
        sent_data = self._format_bytes(device.tx_bytes)
        text_message = (
            f'*Имя устройства: "{device.name}"*\n',
            f"Описание: {device.description}",
            f"Получено: {recieved_data}",
            f"Отправлено: {sent_data}",
            f"Последний IP: {device.remote_ip}",
            f"Последнее рукопожатие: {device.latest_handshake}",
            f"Разрешенные ip: {device.allowed_ips}",
            f"DNS: {device.dns}",
            f"Endpoint: `{device.endpoint}`",
            f"MTU: {device.mtu}",
            f"Public key: `{device.public_key}`",
            f"Preshared Key: `{device.preshared_key}`",
        )
        text_message = "\n- ".join(text_message)
        text_message = escaping(text_message)
        return text_message

    @staticmethod
    def _format_bytes(size: int) -> str:
        """
        Приводит к читаемому виду байты
        """
        if size is None:
            return f"0 B"
        power = 2 ** 10
        n = 0
        power_labels = {0: "", 1: "Kb", 2: "Mb", 3: "Gb", 4: "Tb"}
        while size > power:
            size /= power
            n += 1
        string = f"{round(size, 2):,} {power_labels[n]}".replace(",", "")
        return string

    async def device_confirm_delete(self, callback_query: CallbackQuery, state: FSMContext):
        """Подтверждение удаления устройства"""
        device_id = extract_id_from_callback_data(callback_query)
        device = await self._api.get_device_by_id(device_id=device_id)
        text_message = self._create_device_details_message(device=device)
        text_message += "\n\n*Удалить?*"
        keyboard = InlineKeyboardMarkup()
        device_details_prefix = self.__class__.device_details_prefix
        delete_device_prefix = self.__class__.delete_device_prefix
        keyboard.add(
            InlineKeyboardButton("Да", callback_data=f"/{delete_device_prefix}_<id:{device_id}>"),
            InlineKeyboardButton("Отмена", callback_data=f"/{device_details_prefix}_<id:{device_id}>_<edit>"),
        )
        await callback_query.message.edit_text(text_message, reply_markup=keyboard, parse_mode="MarkdownV2")

    async def delete_device(self, callback_query: CallbackQuery, state: FSMContext):
        device_id = extract_id_from_callback_data(callback_query)
        device = await self._api.get_device_by_id(device_id=device_id)
        fz_user_id = device.user_id
        await self._api.delete_device(device_id=device_id)
        await asyncio.gather(
            callback_query.answer(f'Устройство "{device.name}" удалено'),
            self.list_devices(callback_query=callback_query, state=state, fz_user_id=fz_user_id),
        )
