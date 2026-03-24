from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dependencies import state_change, get_order_repo
from order_repo import OrderRepository

app = FastAPI()

@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs")

# define test state versus live state
state_change(app, "prod") # "dev" or "prod"

class OrderCreate(BaseModel):
    shipping: float
    tax_rate: float
    items: dict[str, int]

@app.post("/api/order")
def create_order(user_id: int, order_data: OrderCreate, repo: OrderRepository = Depends(get_order_repo)):
    return_details = repo.create_order(user_id=user_id, order_data=order_data)
    return return_details

@app.get("/api/order")
def get_order_status(user_id: int, order_id: int, repo: OrderRepository = Depends(get_order_repo)):
    return_details = repo.get_order_status(user_id=user_id, order_id=order_id)
    return return_details

@app.post("/api/order/{id}")
def cancel_order(user_id: int, order_id: int, repo: OrderRepository = Depends(get_order_repo)):
    return_details = repo.cancel_order(user_id=user_id, order_id=order_id)
    return return_details

@app.get("/api/order/{id}")
def get_order_itemized(user_id: int, order_id: int, repo: OrderRepository = Depends(get_order_repo)):
    return_details = repo.get_order_itemized(user_id=user_id, order_id=order_id)
    return return_details
