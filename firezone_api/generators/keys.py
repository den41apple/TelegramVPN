"""
Генератор секретных ключей
"""
from pywgkey.key import WgKey, WgPsk


class KeysGenerator:
    def __init__(self):
        self.public_key: str = None
        self.private_key: str = None
        self.preshared_key: str = None

    def generate(self):
        keys_pair = WgKey()
        psk_key = WgPsk()
        self.public_key = keys_pair.privkey
        self.private_key = keys_pair.pubkey
        self.preshared_key = psk_key.key
