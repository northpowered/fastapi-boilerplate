import hashlib

PASSWORD_SALT: str = '79fd39c66d3_MY_INSECURE_SALT_453722dfb0b38148f4f0905b722283f269d2700dd4d753d'
PASSWORD_ALGORITHM: str = 'sha512'
PASSWORD_ITERATIONS: int = 100000


def create_password_hash(plaintext: str) -> str:
    return hashlib.pbkdf2_hmac(
        PASSWORD_ALGORITHM,
        plaintext.encode('utf-8'),
        PASSWORD_SALT.encode('utf-8'),
        PASSWORD_ITERATIONS
    ).hex()
