"""
Модуль API-эндпоинтов для управления пользователями и аутентификации
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse, Token, UserMessage
from app.auth.dependencies import get_current_user
from app.auth.auth_handler import (get_password_hash, verify_password, create_access_token)
from app.database import get_db

router = APIRouter(tags=["Пользователи"])


@router.post("/register", response_model=UserMessage)
async def register_user(
        user_data: UserCreate,
        db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя в системе
    """
    existing_user = db.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": f"Пользователь {new_user.username} успешно зарегистрирован",
        "user": new_user
    }


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    Аутентификация пользователя и получение JWT токена
    """
    user = db.exec(select(User).where(User.email == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учётные данные",
        )

    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "token_type": "bearer",
        "message": f"Пользователь {user.username} успешно вошёл в систему"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
        current_user: User = Depends(get_current_user)
):
    """
    Получение профиля текущего авторизованного пользователя
    """
    return current_user
