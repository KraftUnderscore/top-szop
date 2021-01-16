from django.test import TestCase
from server.database_operations import cart, product, order, delivery

class ModelsTestCase(TestCase):

    def setUp(self):
        cart.add_cart()
        product.add_product("Telewizor", "Opis telewizora", 1234.56)
        product.add_product("Aparat", "Opis aparatu", 653.12)
        product.add_product("Komputer", "Opis komputera", 5944.95)
        cart.add_product_to_cart(5, 1)
        cart.add_product_to_cart(3, 2)
        cart.add_product_to_cart(7, 3)
        order.add_order("admin@admin.com")
        delivery.add_delivery(1, "ul. Warszawska 17, Wrocław")

    def test_add_delivery_incorrect_order(self):
        """Try adding Delivery for Order that doesn't exist"""

        out = delivery.add_delivery(100, "ul. Warszawska 17, Wrocław")

        self.assertFalse(out)

    def test_get_delivery_data(self):
        """Try getting delivery data from existing Delivery"""

        order, info = delivery.get_delivery_data(1)

        self.assertEqual(info, "ul. Warszawska 17, Wrocław")

        products = order['products']
        amounts = order['amounts']
        order_date = order['order_date']
        total_cost = order['total_cost']
        email = order['email']

        self.assertEqual(len(products), 3)
        self.assertEqual(amounts, [5, 3, 7])
        self.assertAlmostEqual(total_cost, 1234.56 * 5 + 653.12 * 3 + 5944.95 * 7)
        self.assertEqual(email, "admin@admin.com")

    def test_get_delivery_data_incorrect_delivery(self):
        """Try getting delivery data from non-existing Delivery"""

        order, info = delivery.get_delivery_data(100)

        self.assertIsNone(order)
        self.assertIsNone(info)
