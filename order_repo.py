from abc import ABC, abstractmethod

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