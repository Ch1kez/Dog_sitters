
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Модель данных для создания заказа
class OrderCreate(BaseModel):
    apartment_number: int
    pet_name: str
    breed: str
    walk_time: datetime
    duration_minutes: int

# Модель данных для ответа на запрос о заказе
class OrderResponse(BaseModel):
    id: int
    apartment_number: int
    pet_name: str
    breed: str
    walk_time: datetime
    duration_minutes: int

    class Config:
        orm_mode = True
