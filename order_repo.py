from abc import ABC, abstractmethod
import random
import datetime
from datetime import date

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
        
class OrderRepository(ABC):

    @abstractmethod
    def create_order():
        pass

    @abstractmethod
    def get_order_status():
        pass

    @abstractmethod
    def cancel_order():
        pass

    @abstractmethod
    def get_order_itemized():
        pass
