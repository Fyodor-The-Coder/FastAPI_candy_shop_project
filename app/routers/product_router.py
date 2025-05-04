"""
Модуль API-эндпоинтов для управления товарами магазина.
Содержит операции CRUD (Create, Read, Update, Delete) для работы с товарами
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product_schema import \
    (ProductCreate, ProductResponse, ProductUpdate, ProductShortInfo)
from app.database import get_db

router = APIRouter(tags=["Товары"])

@router.post(
    "/create_a_new_product_item",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db),
):
    """"
    Создание нового товара в каталоге
    """
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/view_all_products", response_model=List[ProductShortInfo])
def get_all_products(db: Session = Depends(get_db)):
    """
    Получение списка всех товаров с краткой информацией
    """
    return db.query(Product).all()


@router.get("/get_product_by_ID", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """"
    Получение полной информации о товаре по ID
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    return product


@router.put("/update_product_by_ID/{product_id}", response_model=ProductResponse)
def update_product(
        product_id: int,
        product_data: ProductUpdate,
        db: Session = Depends(get_db),
):
    """"
    Обновление данных товара
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product



@router.delete("/delete_product_by_ID", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
):
    """"
    Удаление товара из системы
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    db.delete(db_product)
    db.commit()
