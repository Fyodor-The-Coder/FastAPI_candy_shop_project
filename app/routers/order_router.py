from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.product import Product
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
def create_order(
        order: OrderCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    product = db.query(Product).get(order.product_id)

    if not product:
        raise HTTPException(404, "Товар не найден")

    if product.stock < order.quantity:
        # todo business-logic
        raise HTTPException(400, "Недостаточное количество товара на складе")

    db_order = Order(
        user_id=user.id,
        product_id=product.id,
        quantity=order.quantity
    )

    product.stock -= order.quantity
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
