from order_repo import OrderRepository
import random
import datetime
from datetime import date
import logging

log = logging.getLogger("Activity Log")
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("activity.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s","%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

class Order():
    def __init__(self, order_id, order_shipping, order_tax, user_id):
        self.id = order_id
        self.number = str(random.randrange(1000000000, 9999999999))
        self.date = str(date.today())
        self.time = str(datetime.datetime.now().time().strftime("%H:%M:%S"))
        self.shipping = order_shipping
        self.tax = order_tax
        self.pre_total = 0.0
        self.tax_value = 0.0
        self.total = 0.0
        self.user = user_id
        self.status = 'Not Shipped'
        self.items = {}

class DevOrderRepository(OrderRepository):
    def __init__(self):
        self.users = {1: ('JOHN', 'CARTER', '555-214-8890', 'john.carter@example.com', '102 Maple Ridge Dr, Austin, TX 78721'),
                        2: ('MARIA', 'SANCHEZ', '555-771-0042', 'maria.sanchez@example.com', '88 Willow Bend Ln, Phoenix, AZ 85016'),
                        3: ('DAVID', 'NGUYEN', '555-903-1128', 'david.nguyen@example.com', '450 Sunset Park Blvd, Denver, CO 80205'),
                        4: ('EMILY', 'ROBERTS', '555-642-7781', 'emily.roberts@example.com', '12 Brookside Terrace, Portland, OR 97206'),
                        5: ('MICHAEL', 'THOMPSON', '555-330-9922', 'michael.thompson@example.com', '760 Lakeview Ct, Chicago, IL 60614'),
                        6: ('SARAH', 'PATEL', '555-118-4477', 'sarah.patel@example.com', '55 Orchard Hill Rd, Atlanta, GA 30309'),
                        7: ('KEVIN', 'WILSON', '555-889-2204', 'kevin.wilson@example.com', '901 Cedar Grove St, Columbus, OH 43215'),
                        8: ('LINDA', 'MARTIN', '555-447-6610', 'linda.martin@example.com', '33 Pine Hollow Ave, Tampa, FL 33611'),
                        9: ('ROBERT', 'HARRIS', '555-702-5533', 'robert.harris@example.com', '284 Oak Meadow Dr, Nashville, TN 37211'),
                        10: ('JESSICA', 'LEE', '555-990-7744', 'jessica.lee@example.com', '19 Evergreen Crest, Seattle, WA 98115')}
        self.products = {1: ('WIRELESS MOUSE', '012345678905', 19.99),
                        2: ('MECHANICAL KEYBOARD', '098765432112', 89.50),
                        3: ('USB-C CHARGING CABLE', '123450987654', 12.99),
                        4: ('27" LED MONITOR', '445566778899', 179.00),
                        5: ('BLUETOOTH HEADPHONES', '556677889900', 59.95),
                        6: ('EXTERNAL HARD DRIVE 1TB', '667788990011', 74.99),
                        7: ('LAPTOP STAND', '778899001122', 29.50),
                        8: ('PORTABLE POWER BANK 10,000MAH', '889900112233', 24.99),
                        9: ('HDMI 2.1 CABLE', '990011223344', 14.49),
                        10: ('SMART DESK LAMP', '101112131415', 39.99),
                        11: ('WIRELESS EARBUDS', '121314151617', 49.99),
                        12: ('GAMING CONTROLLER', '131415161718', 64.99),
                        13: ('500GB SSD', '141516171819', 52.00),
                        14: ('OFFICE CHAIR CUSHION', '151617181920', 22.95),
                        15: ('NOISE-CANCELING HEADSET', '161718192021', 129.99),
                        16: ('WEB CAMERA 1080P', '171819202122', 34.99),
                        17: ('MINI BLUETOOTH SPEAKER', '181920212223', 27.49),
                        18: ('SURGE PROTECTOR 6-OUTLET', '192021222324', 18.75),
                        19: ('WIRELESS KEYBOARD', '202122232425', 32.99),
                        20: ('ADJUSTABLE PHONE STAND', '212223242526', 9.99)}
        self.orders = {}
        self.next_order_id = 1

    def create_order(self, user_id: int, order_data: object) -> str:
        order_id = self.next_order_id
        order_shipping = order_data.shipping
        order_tax = order_data.tax_rate
        product_data = {}
        for item, quantity in order_data.items.items():
            for product in self.products.values():
                if item in product:
                    product_data[item] = (product[0], quantity, product[2])
                    break
            else:
                log.error(f"User ID: {user_id}, Item {item} not found or out of stock")
                return {"Error": f"Item '{item}' not found or out of stock"}
        order = Order(order_id, order_shipping, order_tax, user_id)
        order.items = product_data
        itemized_total = []
        item_total = []
        order_value = 0.0
        for item in order.items.values():
            item_total = item[1] * item[2]
            itemized_total.append(item_total)
            item_total = []
        for total in itemized_total:
            order_value += total
        order.pre_total = order_value
        order_tax_value = order_value*order.tax
        order.tax_value = f'{round(order_tax_value-order.pre_total, 2):.2f}'
        order_value = order_tax_value+order.shipping
        order.total = f'{round(order_value, 2):.2f}'

        self.orders[order_id] = order
        self.next_order_id += 1

        log.info(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order ID {order.id} Placed")
        return {"Success": "Order Placed", "order_id": order.id, "order_number": order.number, "order_date": order.date, "order_time": order.time, "order_shipping": order.shipping, "order_tax": order.tax_value, "order_total": order.total, "order_status": order.status}

    def get_order_status(self, user_id: int, order_id: int) -> str:
        if order_id in self.orders:
            order = self.orders[order_id]
            log.info(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order ID {order.id} Status Retrieved")
            return {"order_number": order.number, "order_date": order.date, "order_time": order.time, "order_total": order.total, "order_status": order.status}
        else:
            log.error(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order {order_id} Not Found")
            return {"Failure": "Order Not Found"}

    def cancel_order(self, user_id: int, order_id: int) -> str:
        if order_id in self.orders:
            order = self.orders[order_id]
            if order.status == 'Not Shipped':
                order.status = 'Cancelled'
                log.info(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order ID {order.id} Cancelled")
                return {"success": "Your order has been cancelled", "order_number": order.number, "order_date": order.date, "order_time": order.time, "order_total": order.total, "order_status": order.status}
            else:
                log.error(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order {order_id} could not be cancelled.")
                return {"Failure": "Order could not be cancelled."}
        else:
            log.error(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order {order_id} Not Found")
            return {"Failure": "Order Not Found"}

    def get_order_itemized(self, user_id: int, order_id: int) -> str:
        if order_id in self.orders.keys():
            order = self.orders[order_id]
        else:
            log.error(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order {order_id} Not Found")
            return {"Failure": "Order Not Found"}
        order_itemized = {}
        for item, details in order.items.items():
            for pid, product in self.products.items():
                if item in product:
                    id = pid
            item_details = {"upc": item, "name": details[0], "quantity": details[1], "cost": f"{details[1]*details[2]:.2F}"}
            order_itemized[id] = item_details
        log.info(f"{date.today()} {datetime.datetime.now().time().strftime("%H:%M:%S")}, User ID: {user_id}, Order ID {order.id} Itemization Retrieved")
        return {"order_number": order.number, "order_date": order.date, "order_time": order.time, "order_shipping": order.shipping, "order_tax": order.tax_value, "order_total": order.total, "order_status": order.status, "order_items": order_itemized}