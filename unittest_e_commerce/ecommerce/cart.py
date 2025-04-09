# ecommerce/cart.py
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.items.append({"item": item, "quantity": quantity})

    def remove_item(self, item):
        self.items = [i for i in self.items if i['item'] != item]

    def get_total_items(self):
        return sum(i['quantity'] for i in self.items)

    def calculate_total_price(self):
        return sum(i['item'].price * i['quantity'] for i in self.items)


class Item:
    def __init__(self, name, price):
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        self.name = name
        self.price = price