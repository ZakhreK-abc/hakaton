from cryptography.fernet import Fernet, InvalidToken
from pydantic_settings import BaseSettings
from app.core.config import settings

class DataEncryptor:
    def __init__(self, key: str):
        self.fernet = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        """Возвращает base64-строку"""
        if not data:
            return ""
        encrypted = self.fernet.encrypt(data.encode())
        return encrypted.decode()

    def decrypt(self, encrypted: str) -> str:
        if not encrypted:
            return ""
        try:
            decrypted = self.fernet.decrypt(encrypted.encode())
            return decrypted.decode()
        except InvalidToken:
            raise ValueError("Невозможно расшифровать данные (неверный ключ или повреждены)")


# Глобальный экземпляр (или можно внедрять через Depends)
encryptor = DataEncryptor(settings.SECRET_KEY)