from sqlalchemy import Column, Integer, String, Float, JSON
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    ingredients = Column(JSON, nullable=False)  # Пример: ["сахар", "мука", "яйца"]
    stock = Column(Integer, default=0)