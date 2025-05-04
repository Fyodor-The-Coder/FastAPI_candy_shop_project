"""
Главный модуль приложения для управления складом кондитерского магазина.
Содержит конфигурацию основного приложения FastAPI и подключение роутеров
"""

from fastapi import FastAPI
from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router

app = FastAPI(
    title="Система управления складом кондитерского магазина",
    description="Простейшая система управления складом кондитерского магазина, основанная на"
                "веб-фреймворке FastAPI",
    version="0.0.1",
    contact={
        "url": "https://github.com/Fyodor-The-Coder",
        "email": "fyodor.konto2@gmail.com"
    }
)


@app.get("/")
def root():
    """Проверочный эндпоинт для тестирования работы API"""
    return {"message": "Hello, world!"}

app.include_router(user_router, prefix="/auth")
app.include_router(product_router, prefix="/products")
app.include_router(order_router, prefix="/orders")
