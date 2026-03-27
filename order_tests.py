import unittest
import time
from dev_repo import DevOrderRepository
from db_repo import DBOrderRepository

state = "dev" # "dev" or "prod"

if state == "dev":
    repo = DevOrderRepository()
elif state == "prod":
    repo = DBOrderRepository()

class OrderCreate():
    def __init__(self):
        self.shipping = 5.99
        self.tax_rate = 1.06
        self.items = {
    "012345678905": 1,
    "098765432112": 2,
    "123450987654": 1,
    "445566778899": 3,
    "556677889900": 1,
    "667788990011": 1,
    "778899001122": 2,
    "889900112233": 1,
    "990011223344": 2,
    "101112131415": 1,
    "121314151617": 1,
    "131415161718": 1,
    "141516171819": 2,
    "151617181920": 1,
    "161718192021": 1,
    "171819202122": 1,
    "181920212223": 2,
    "192021222324": 1,
    "202122232425": 1,
    "212223242526": 3
}
        
order = OrderCreate()

class TestCreateOrderFunction(unittest.TestCase):
    
    def test_create_order(self):
        start_time = time.perf_counter()
        repo.create_order(user_id=1, order_data=order)
        end_time = time.perf_counter()
        response_time = end_time-start_time
        # Prod Database performs 6 queries - test measures 200ms response per query
        self.assertLess(response_time, 1.2, f"Response time was too slow: {response_time}s")

class TestGetOrderStatusFunction(unittest.TestCase):

    def test_get_order_status(self):
        start_time = time.perf_counter()
        repo.get_order_status(user_id=1, order_id=1)
        end_time = time.perf_counter()
        response_time = end_time-start_time
        # Prod Database performs 1 query - test measures 200ms response per query
        self.assertLess(response_time, 0.2, f"Response time was too slow: {response_time}s")

class TestCancelOrderFunction(unittest.TestCase):

    def test_cancel_order(self):
        start_time = time.perf_counter()
        repo.cancel_order(user_id=1, order_id=1)
        end_time = time.perf_counter()
        response_time = end_time-start_time
        # Prod Database performs 3 queries - test measures 200ms response per query
        self.assertLess(response_time, 0.6, f"Response time was too slow: {response_time}s")

class TestGetOrderItemizedFunction(unittest.TestCase):

    def test_get_order_itemized(self):
        start_time = time.perf_counter()
        repo.get_order_status(user_id=1, order_id=1)
        end_time = time.perf_counter()
        response_time = end_time-start_time
        # Prod Database performs 1 query - test measures 200ms response per query
        self.assertLess(response_time, 0.2, f"Response time was too slow: {response_time}s")

if __name__ == '__main__':
    unittest.main()
