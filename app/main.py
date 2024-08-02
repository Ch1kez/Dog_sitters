
from fastapi import FastAPI
from app.routers import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    print("Application startup")

@app.on_event("shutdown")
async def shutdown():
    print("Application shutdown")
