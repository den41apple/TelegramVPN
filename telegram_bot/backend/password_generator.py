import random


def generate_password(length: int = 20) -> str:
    """Генерирует случайный пароль"""
    digits = '1234567890'
    leters = 'abcdefghijklmnopqrstuvwxyz'
    leters_upper = leters.upper()
    spec_symbols = '!@#$%^&*()-+~'
    all_symbols = digits + leters + leters_upper + spec_symbols
    password = [random.choice(all_symbols) for _ in range(length)]
    return ''.join(password)
