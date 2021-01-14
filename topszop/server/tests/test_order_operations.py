from django.test import TestCase
from server.database_operations import product, cart, order
from server.models import Product, Cart, Cart_Product

class OrderTestCase(TestCase):
    def setUp(self):
        cart.add_cart()
        product.add_product("Telewizor", "Opis telewizora", 1234.56)
        product.add_product("Aparat", "Opis aparatu", 653.12)
        product.add_product("Komputer", "Opis komputera", 5944.95)
        cart.add_product_to_cart(5, 1)
        cart.add_product_to_cart(3, 2)
        cart.add_product_to_cart(7, 3)
        order.add_order("admin@admin.com")

    def test_add_order_empty_cart(self):
        """Try to add an Order for a Cart with no Products"""

        cart.add_cart()
        out = order.add_order("admin@admin.com", 2)

        self.assertFalse(out)

    def test_add_order_invalid_cart(self):
        """Try to add an Order for a non-existing Cart"""

        out = order.add_order("admin@admin.com", 2)

        self.assertFalse(out)

    def test_add_order_invalid_email(self):
        """Try to add an Order for invalid email"""

        out = order.add_order("bad_mail")

        self.assertFalse(out)

    def test_get_order_data(self):
        """Try to get Order's data by order_id"""

        data = order.get_order_data()

        products = data['products']
        amounts = data['amounts']
        order_date = data['order_date']
        total_cost = data['total_cost']
        email = data['email']

        self.assertEqual(len(products), 3)
        self.assertAlmostEqual(total_cost, 1234.56 * 5 + 653.12 * 3 + 5944.95 * 7)
        self.assertEqual(email, "admin@admin.com")

    def test_get_incorrect_order_data(self):
        """Try to get Order's data with incorrect order_id"""

        data = order.get_order_data(56)

        self.assertIsNone(data)


