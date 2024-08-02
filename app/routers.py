# app/routers.py

from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db, close_db
from app.models import OrderCreate, OrderResponse
import asyncpg

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    conn = await get_db()
    try:
        query = """
        INSERT INTO orders (apartment_number, pet_name, breed, walk_time, duration_minutes)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        order_id = await conn.fetchval(query, order.apartment_number, order.pet_name, order.breed, order.walk_time, order.duration_minutes)
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
