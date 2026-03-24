from order_repo import Order, OrderRepository
import os
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()

log = logging.getLogger("Activity Log")
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("activity.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s","%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

def db_connect():
    DATABASE = os.getenv("DATABASE")
    USERNAME = os.getenv("USERNAME")
    PWD = os.getenv("PWD")
    conn = psycopg2.connect(f'dbname={DATABASE} user={USERNAME} password={PWD}')
    cur = conn.cursor()
    return cur, conn

def db_disconnect(cur, conn):
    cur.close() 
    conn.close()

class DBOrderRepository(OrderRepository):

    def create_order(self, user_id: int, order_data: object) -> str:
        order_id = None
        order_shipping = order_data.shipping
        order_tax = order_data.tax_rate

        order = Order(order_id, order_shipping, order_tax, user_id)
        cur, conn = db_connect()
        try:
            with conn, cur:
                cur.execute("SELECT * FROM CreateNewOrder(%s, %s, %s, %s, %s);",
                (user_id, order.date, order.time, order.shipping, order.tax))
                query = cur.fetchall()
                order.id = query[0][0]
            
                for item, quantity in order_data.items.items():
                    cur.execute("SELECT * FROM CreateOrderItem(%s, %s, %s);",
                    (order.id, item, quantity))

                cur.execute("SELECT * FROM CalculateOrderPreTotal(%s);",
                (order.id,))
                query = cur.fetchall()
                query = query[0][0]
                order.pre_total = float(query)
                order_tax_value = order.pre_total*order.tax
                order.tax_value = f'{round(order_tax_value-order.pre_total, 2):.2f}'
                order_value = order_tax_value+order.shipping
                order.total = f'{round(order_value, 2):.2f}'
            
                cur.execute("SELECT * FROM UpdateOrderTotals(%s, %s, %s, %s);",
                (order.id, order.pre_total, order.tax_value, order.total))
                query = cur.fetchall()
        except Exception as e:
            log.error(e)
            return {"Error while creating order. Please try again later"}
        finally:
            db_disconnect(cur, conn)

        log.info(f'User ID: {user_id}, Order ID {order.id} Placed')
        return {"Success": "Order Placed", "order_id": order.id, "order_number": order.number, "order_date": order.date, "order_time": order.time, "order_shipping": order.shipping, "order_tax": order.tax_value, "order_total": order.total, "order_status": order.status}

    def get_order_status(self, user_id: int, order_id: int) -> str:
        cur, conn = db_connect()
        try:
            with conn, cur:
                cur.execute("SELECT * FROM GetOrderStatus(%s);",
                (order_id,))
                query = cur.fetchall()
                query = query[0]
                order = Order(order_id=order_id, order_shipping=0.0, order_tax=0.0, user_id=user_id)
                order.number = query[1]
                order.date = query[2]
                order.time = query[3]
                order.status = query[6]
                order.total = f"{query[7]:.2F}"
        except Exception as e:
            log.error(e)
            return {"Order Not Found"}
        finally:
            db_disconnect(cur, conn)
            
        log.info(f"User ID: {user_id}, Order ID {order.id} Status Retrieved")
        return {"order_id": order.id, "order_number": order.number, "order_date": order.date, "order_time": order.time, "order_total": order.total, "order_status": order.status}

    def cancel_order(self, user_id: int, order_id: int) -> str:
        cur, conn = db_connect()
        try:
            with conn, cur:
                cur.execute("SELECT * FROM CancelCustomerOrder(%s);",
                (order_id,))
                query = cur.fetchall()
                query = query[0]
                order = Order(order_id=order_id, order_shipping=0.0, order_tax=0.0, user_id=user_id)
                order.number = query[1]
                order.date = query[2]
                order.time = query[3]
                order.status = query[4]
                order.total = f"{query[5]:.2F}"
        except Exception as e:
            log.error(e)
            return {"Unable to cancel order or order not found."}
        finally:
            db_disconnect(cur, conn)
            
        log.info(f'User ID: {user_id}, Order ID {order.id} Placed')
        return {"success": "Your order has been cancelled", "oder_id": order.id, "order_number": order.number, "order_date": order.date, "order_time": order.time, "order_total": order.total, "order_status": order.status}

    def get_order_itemized(self, user_id: int, order_id: int) -> str:
        cur, conn = db_connect()
        try:
            with conn, cur:
                cur.execute("SELECT * FROM GetOrderStatus(%s);",
                (order_id,))
                query = cur.fetchall()
                query = query[0]
                order = Order(order_id=order_id, order_shipping=0.0, order_tax=0.0, user_id=user_id)
                order.number = query[1]
                order.date = query[2]
                order.time = query[3]
                order.shipping = query[4]
                order.tax_value = query[5]
                order.status = query[6]
                order.total = f"{query[7]:.2F}"

                cur.execute("SELECT * FROM GetOrderItemization(%s);",
                (order_id,))
                query = cur.fetchall()
                order_itemized = {}
                for item in query:
                    item_details = {"upc": item[2], "name": item[1], "quantity": item[4], "cost": f"{item[5]:.2F}"}
                    order_itemized[item[0]] = item_details
        except Exception as e:
            log.error(e)
            return {"Order Not Found"}
        finally:
            db_disconnect(cur, conn)
            
        log.info(f'User ID: {user_id}, Order ID {order.id} Placed')
        return {"order_number": order.number, "order_date": order.date, "order_time": order.time, "order_shipping": order.shipping, "order_tax": order.tax_value, "order_total": order.total, "order_status": order.status, "order_items": order_itemized}
