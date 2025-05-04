from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.schemas.order_schema import OrderResponse, OrderItemCreate
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.business_logic.recommendations import RecommendationEngine
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product
from typing import List

router = APIRouter(tags=["orders"])


def get_order_or_404(order_id: int, db: Session, user: User):
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).get(order_id)

    if not order or order.user_id != user.id:
        raise HTTPException(404, "Заказ не найден")

    return order


@router.get("/get_all_orders", response_model=List[OrderResponse],
            summary="Получить все заказы пользователя")
def get_all_orders(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    Возвращает список всех заказов текущего пользователя.

    Включает полную информацию по каждому заказу:
    - ID заказа
    - Статус
    - Дата создания
    - Список товаров с ценами и количеством
    """
    orders = (
        db.query(Order)
        .options(
            joinedload(Order.items)
            .joinedload(OrderItem.product)
        )
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return orders


@router.get("/get_the_order_using_ID", response_model=OrderResponse, summary="Получить заказ по ID")
def get_order(
        order_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    Возвращает детальную информацию о конкретном заказе по его ID.

    Требования:
    - Заказ должен принадлежать текущему пользователю
    - Заказ должен существовать

    Возвращает 404 ошибку если заказ не найден или нет прав доступа
    """
    order = (
        db.query(Order)
        .options(
            joinedload(Order.items)
            .joinedload(OrderItem.product)
        )
        .filter(Order.id == order_id)
        .first()
    )

    if not order or order.user_id != user.id:
        raise HTTPException(
            status_code=404,
            detail="Заказ не найден или у вас нет прав доступа"
        )

    return order

@router.post("/create_new_order", response_model=OrderResponse)
def create_order(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    Создание нового пустого заказа
    """
    db_order = Order(user_id=user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.post("/add_new_order_item", response_model=OrderResponse)
def add_order_item(
        order_id: int,
        item: OrderItemCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    order = get_order_or_404(order_id, db, user)
    product = db.query(Product).get(item.product_id)

    if not product:
        raise HTTPException(404, "Товар не найден")

    if product.stock < item.quantity:
        recommender = RecommendationEngine(db)
        alternatives = recommender.find_alternatives(item.product_id)
        raise HTTPException(409, detail=recommender.prepare_recommendation_message(alternatives))

    try:
        db_item = OrderItem(**item.model_dump(), order_id=order_id)
        product.stock -= item.quantity
        db.add(db_item)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Товар уже в заказе")

    db.refresh(order)
    return order


@router.put("/update_order_item", response_model=OrderResponse)
def update_order_item(
        order_id: int,
        item_id: int,
        quantity: int = Body(..., gt=0,example=2,
        description="Новое количество товара (должно быть больше 0"),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    order = get_order_or_404(order_id, db, user)
    item = next((i for i in order.items if i.id == item_id), None)

    if not item:
        raise HTTPException(404, "Позиция не найдена")

    delta = quantity - item.quantity
    product = db.query(Product).get(item.product_id)

    if product.stock < delta:
        recommender = RecommendationEngine(db)
        alternatives = recommender.find_alternatives(item.product_id)
        raise HTTPException(409, detail=recommender.prepare_recommendation_message(alternatives))

    product.stock -= delta
    item.quantity = quantity
    db.commit()
    db.refresh(order)
    return order


@router.delete("/remove_order_item", response_model=OrderResponse)
def remove_order_item(
        order_id: int,
        item_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    order = get_order_or_404(order_id, db, user)
    item = next((i for i in order.items if i.id == item_id), None)

    if not item:
        raise HTTPException(404, "Позиция не найдена")

    product = db.query(Product).get(item.product_id)
    product.stock += item.quantity
    db.delete(item)
    db.commit()
    db.refresh(order)
    return order
