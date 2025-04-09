# tests/test_cart.py
import unittest
from unittest.mock import Mock
from ecommerce.cart import Cart, Item


class TestCart(unittest.TestCase):
    def setUp(self):
        # Set up a fresh Cart object before each test.
        self.cart = Cart()

    def test_add_item(self):
        # Test adding an item to the cart."""""
        item = Item("Laptop", 999.99)
        self.cart.add_item(item, 2)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]["item"], item)
        self.assertEqual(self.cart.items[0]["quantity"], 2)

    def test_remove_item(self):
        # Test removing an item from the cart.
        item1 = Item("Laptop", 999.99)
        item2 = Item("Phone", 599.99)
        self.cart.add_item(item1, 1)
        self.cart.add_item(item2, 2)
        self.cart.remove_item(item1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]["item"], item2)

    def test_get_total_items(self):
        # Test getting the total number of items in the cart.
        item = Item("Tablet", 200)
        self.cart.add_item(item, 3)
        self.assertEqual(self.cart.get_total_items(), 3)

    def test_calculate_total_price(self):
        # Test calculating the total price of items in the cart.
        item1 = Mock(name="Laptop", price=1000)
        item2 = Mock(name="Mouse", price=50)
        self.cart.add_item(item1, 2)
        self.cart.add_item(item2, 4)

        total_price = self.cart.calculate_total_price()
        self.assertEqual(total_price, 2200)

    def test_add_item_invalid_quantity(self):
        # Test adding an item with invalid quantity.
        item = Item("Headphones", 100)
        with self.assertRaises(ValueError):
            self.cart.add_item(item, 0)

    def test_item_price_validation(self):
        # Test that item price must be greater than 0.
        with self.assertRaises(ValueError):
            Item("InvalidItem", 0)


if __name__ == "__main__":
    unittest.main()