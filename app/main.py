# app/main.py

from fastapi import FastAPI
from app.routers import router
import asyncio
from init_db import create_database_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_database_and_tables()
    print("Application startup")

@app.on_event("shutdown")
async def shutdown():
    print("Application shutdown")

app.include_router(router)
