from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    orders: List["Order"] = Relationship(back_populates="user")
