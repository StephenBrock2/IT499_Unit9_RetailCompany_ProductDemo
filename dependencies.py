from fastapi import Request
from dev_repo import DevOrderRepository
from db_repo import DBOrderRepository

def state_change(app, state: str):
    app.state.env = state
    if state == 'dev':
        app.state.order_repo = DevOrderRepository()
    elif state == 'prod':
        app.state.order_repo = DBOrderRepository()

def get_order_repo(request: Request):
    return request.app.state.order_repo