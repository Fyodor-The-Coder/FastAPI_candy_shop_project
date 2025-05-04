from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.order import Order

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db

    def find_alternatives(self, original_product_id: int, excluded_ids: List[int] = None) -> List[Product]:
        original_product = self.db.query(Product).get(original_product_id)
        if not original_product:
            return []

        same_category = self.db.query(Product).filter(
            Product.category == original_product.category,
            Product.id != original_product_id,
            Product.id.notin_(excluded_ids or []),
            Product.stock > 0
        ).all()

        ranked_products = []
        for product in same_category:
            common_ingredients = set(original_product.ingredients) & set(product.ingredients)
            ranked_products.append((-len(common_ingredients), product))

        # Исправленная сортировка
        ranked_products.sort(key=lambda x: x[0])

        result = [p[1] for p in ranked_products[:3]]

        if len(result) < 3:
            additional = self.db.query(Product).filter(
                Product.id.notin_([p.id for p in result] + [original_product_id] + (excluded_ids or [])),
                Product.stock > 0
            ).limit(3 - len(result)).all()
            result += additional

        return result[:3]

    @staticmethod
    def prepare_recommendation_message(products: List[Product]) -> Dict:
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
        recommendations = {}
        for item in order.items:
            product = self.db.query(Product).get(item.product_id)
            if product.stock < item.quantity:
                recs = self.find_alternatives(item.product_id)
                recommendations[item.product_id] = recs
        return recommendations
