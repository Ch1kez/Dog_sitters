from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db, close_db
from app.models import OrderCreate, OrderResponse
import asyncpg
from datetime import datetime, timedelta

router = APIRouter()


# Проверка времени прогулки
def is_valid_walk_time(walk_time: datetime) -> bool:
    if walk_time.hour < 7 or walk_time.hour > 22:
        return False
    if walk_time.minute not in [0, 30]:
        return False
    return True


# Проверка разницы между текущим временем и временем записи
def is_time_advance_valid(walk_time: datetime) -> bool:
    now = datetime.utcnow()
    if walk_time < now + timedelta(minutes=30):
        return False
    return True


# Проверка занятости Петра и Антона
async def check_availability(conn, walk_time: datetime) -> bool:
    end_time = walk_time + timedelta(minutes=30)
    query = """
    SELECT COUNT(*)
    FROM orders
    WHERE (walk_time < $2 AND walk_time + INTERVAL '30 minutes' > $1)
       OR (walk_time < $1 AND walk_time + INTERVAL '30 minutes' > $1)
    """
    count = await conn.fetchval(query, end_time, walk_time)
    return count < 2  # Проверяем, что максимум два активных заказа


@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    conn = await get_db()
    try:
        if not is_valid_walk_time(order.walk_time):
            raise HTTPException(status_code=400, detail="Invalid walk time.")

        if not is_time_advance_valid(order.walk_time):
            raise HTTPException(status_code=400, detail="Walk time must be at least 30 minutes from now.")

        if not await check_availability(conn, order.walk_time):
            raise HTTPException(status_code=400, detail="Pet sitters are not available at the requested time.")

        query = """
        INSERT INTO orders (apartment_number, pet_name, breed, walk_time, duration_minutes)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        order_id = await conn.fetchval(query, order.apartment_number, order.pet_name, order.breed, order.walk_time,
                                       order.duration_minutes)
        return {**order.dict(), "id": order_id}
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    finally:
        await close_db(conn)


@router.get("/orders/{date}", response_model=list[OrderResponse])
async def get_orders(date: str):
    conn = await get_db()
    try:
        query = """
        SELECT * FROM orders WHERE walk_time::date = $1::date
        """
        rows = await conn.fetch(query, date)
        return [OrderResponse(**dict(row)) for row in rows]
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    finally:
        await close_db(conn)
