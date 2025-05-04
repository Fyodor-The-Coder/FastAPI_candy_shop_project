"""
Модуль схем данных для аутентификации и работы с пользователями
"""
from pydantic import BaseModel

class Token(BaseModel):
    """
    Модель для возврата JWT токена аутентификации.
    Используется в ответах эндпоинтов авторизации
    """
    access_token: str
    token_type: str
    message: str

class UserCreate(BaseModel):
    """
    Модель для регистрации нового пользователя. Входная схема для эндпоинта регистрации
    """
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    """
    Модель ответа с данными пользователя
    """
    # pylint: disable=too-few-public-methods
    id: int
    username: str
    email: str

    class Config:
        """
        Класс, необходимый для совместимости с ORM
        """
        from_attributes = True

class UserMessage(BaseModel):
    """
    Модель для возврата сообщения с данными пользователя.
    Используется в ответах на операции с пользователем
    """
    message: str
    user: UserResponse
