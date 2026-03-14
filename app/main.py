from fastapi import FastAPI
from routers import base

app = FastAPI(
    title="Магазин API",
    version="1.0"
    )

app.include_router(base.router, prefix="/api")

@app.get("/")
def home():
    return {"messege": "home"}