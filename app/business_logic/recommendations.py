"""
Модуль системы рекомендаций для замены товаров при недостатке запасов
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.order import Order

class RecommendationEngine:
    """
    Система рекомендаций товаров для замены при недостатке запасов.

    Основные функции:
    - Поиск альтернативных товаров по категориям и ингредиентам
    - Формирование структурированных рекомендаций
    - Анализ заказов на предмет дефицитных позиций
    """
    def __init__(self, db: Session):
        self.db = db

    def find_alternatives(self, original_product_id: int,
                          excluded_ids: List[int] = None) -> List[Product]:
        """
        Поиск альтернативных товаров для замены.

        Алгоритм работы:
        1. Поиск товаров из той же категории
        2. Ранжирование по количеству общих ингредиентов
        3. Добавление дополнительных товаров при недостатке рекомендаций
        """
        original_product = self.db.query(Product).get(original_product_id)
        if not original_product:
            return []

        same_category = self.db.query(Product).filter(
            Product.category == original_product.category,
            Product.id != original_product_id,
            Product.id.notin_(excluded_ids or []), # pylint: disable=no-member
            Product.stock > 0
        ).all()

        ranked_products = []
        for product in same_category:
            common_ingredients = set(original_product.ingredients) & set(product.ingredients)
            ranked_products.append((-len(common_ingredients), product))

        ranked_products.sort(key=lambda x: x[0])

        result = [p[1] for p in ranked_products[:3]]

        if len(result) < 3:
            additional = self.db.query(Product).filter(
                Product.id.notin_([p.id for p in result] + # pylint: disable=no-member
                                  [original_product_id] + (excluded_ids or [])),
                Product.stock > 0
            ).limit(3 - len(result)).all()
            result += additional

        return result[:3]

    @staticmethod
    def prepare_recommendation_message(products: List[Product]) -> Dict:
        """
        Форматирование рекомендаций для ответа API
        """
        return {
            "detail": "Недостаточно товара на складе",
            "recommendations": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "available_stock": p.stock
                } for p in products
            ]
        }

    def find_alternatives_for_order(self, order: Order):
        """
        Анализ всего заказа на предмет дефицитных позиций
        """
        recommendations = {}
        for item in order.items:
            product = self.db.query(Product).get(item.product_id)
            if product.stock < item.quantity:
                recs = self.find_alternatives(item.product_id)
                recommendations[item.product_id] = recs
        return recommendations
