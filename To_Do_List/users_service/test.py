from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os


def generate_rsa_keys(
    private_key_path="private_key.pem", public_key_path="public_key.pem"
):
    # 1. Генерация приватного ключа
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    # 2. Экспорт приватного ключа в PEM-формат
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),  # Можно использовать шифрование паролем
    )

    # 3. Сохранение приватного ключа в файл
    with open(private_key_path, "wb") as f:
        f.write(private_pem)

    # 4. Извлечение публичного ключа
    public_key = private_key.public_key()

    # 5. Экспорт публичного ключа в PEM-формат
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # 6. Сохранение публичного ключа в файл
    with open(public_key_path, "wb") as f:
        f.write(public_pem)


# Пример использования:
generate_rsa_keys()
