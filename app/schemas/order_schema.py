from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    product_id: int = Field(..., example=1)
    quantity: int = Field(default=1, example=2, ge=1)


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int = Field(..., example=1)
    status: str = Field(
        ...,
        example="created",
        description="Статусы: created, processing, completed, cancelled"
    )
    user_id: int = Field(..., example=1)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [{
                "id": 1,
                "product_id": 1,
                "quantity": 2,
                "status": "created",
                "user_id": 1
            }]
        }
