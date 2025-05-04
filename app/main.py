from fastapi import FastAPI
from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, world!"}

app.include_router(user_router, prefix="/auth")
app.include_router(product_router, prefix="/products")
app.include_router(order_router, prefix="/orders")
