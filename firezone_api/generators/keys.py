"""
Генератор секретных ключей
"""
from wireguard_tools import WireguardKey


class KeysGenerator:
    def __init__(self):
        self.private_key: str = None
        self.public_key: str = None
        self.private_key: str = None

    def generate(self):
        self.private_key = WireguardKey.generate()
        self.public_key = str(self.private_key.public_key())
        self.private_key = str(self.private_key)
