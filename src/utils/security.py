from secrets import token_hex


def generate_random_string_token(bytes: int = 64) -> str:
    return token_hex(bytes)
