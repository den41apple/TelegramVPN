"""
Подготавливает QR код и файл конфигурации
"""
from io import StringIO, BytesIO

from firezone_api.models import Device
from firezone_api.generators import QrCodeGenerator
import configparser

qr_generator = QrCodeGenerator()


def prepare_configuration_qr_and_message(
    device: Device, file_name: str = "EuroHoster.conf"
) -> tuple[StringIO, BytesIO]:
    """
    Подготавливает файл конфигурации и QR код

    Возвращает:
    ----------
        (qr_код, конфигурационный файл)
    """
    config_file, config_string = prepare_config_file(device=device, file_name=file_name)
    qr_generator.generate(config_string)
    qr_file = BytesIO()
    qr_generator.save(qr_file)
    qr_file.seek(0)
    return config_file, qr_file


def prepare_config_file(device: Device, file_name: str) -> tuple[StringIO, str]:
    """
    Подготавливает строку конфигурационного файла
    """
    config = configparser.ConfigParser()
    # Что бы Ключи в нижний регистр не приводил
    config.optionxform = str
    file_object = StringIO()
    address = f"{device.ipv4}/32,{device.ipv6}/128"
    config["Interface"] = {
        "PrivateKey": device.private_key,
        "Address": address,
        "MTU": device.mtu,
        "DNS": ",".join(device.dns),
    }
    config["Peer"] = {
        "PresharedKey": device.preshared_key,
        "PublicKey": device.server_public_key,
        "AllowedIPs": ",".join(device.allowed_ips),
        "Endpoint": device.endpoint,
        "PersistentKeepalive": "25",
    }
    config.write(file_object)
    file_object.seek(0)
    config_string = file_object.read()
    file_object = StringIO(config_string)
    file_object.seek(0)
    file_object.name = file_name
    return file_object, config_string
