from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserMessage(BaseModel):
    message: str
    user: UserResponse