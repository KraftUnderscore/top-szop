from django.test import TestCase
from server.database_operations import product, cart
from server.models import Product, Cart, Cart_Product

class CartTestCase(TestCase):
    def setUp(self):
        product.add_product("Telewizor", "Opis telewizora", 1234.56)
        product.add_product("Pralka", "Opis pralki", 765.43)
        product.add_product("Lodówka", "Opis lodówki", 2631.94)
        cart.add_cart()
        cart.add_product_to_cart(1, "Telewizor") # 1x TV in Cart1
        cart.add_product_to_cart(5, "Pralka") # 5x WM in Cart1
        cart.add_product_to_cart(16, "Lodówka") # 16x Fridge in Cart1

    def test_get_all_products_from_cart(self):
        """Check if correctly gets all products from Cart"""

        prods = cart.get_all_products_from_cart()

        self.assertEqual(len(prods), 3)
        self.assertEqual(prods[0][0], "Telewizor")
        self.assertEqual(prods[1][0], "Pralka")
        self.assertEqual(prods[2][0], "Lodówka")

    def test_get_all_products_from_empty_cart(self):
        """Check if returns empty lists when Cart is empty"""

        cart.add_cart()

        prods = cart.get_all_products_from_cart(cart_id=2)

        self.assertEqual(len(prods), 0)

    def test_set_amount_of_product_in_cart(self):
        """Check if correctly updates amount of product in Cart"""

        out = cart.set_amount_of_product_in_cart(2, "Telewizor")
        prod, amount = cart.get_product_from_cart(1)

        self.assertEqual(amount, 2)
        self.assertTrue(out)

    def test_set_amount_of_incorrect_product_in_cart(self):
        """Check if correctly hanldes updates amount of incorrect product in Cart"""

        out = cart.set_amount_of_product_in_cart(2, 100)

        self.assertFalse(out)

    def test_set_amount_of_product_in_empty_cart(self):
        """Check if correctly hanldes updates amount of product in empty Cart"""

        cart.add_cart()
        out = cart.set_amount_of_product_in_cart(2, "Telewizor", 2)

        self.assertFalse(out)

    def test_add_product_to_cart(self):
        """Check if correctly adds product to Cart"""

        product.add_product("Monitor", "Opis monitora", 777.77)
        out = cart.add_product_to_cart(7, "Monitor")
        prod, amount = cart.get_product_from_cart(4)

        self.assertTrue(out)
        self.assertEqual(amount, 7)
        self.assertEqual(prod.name, "Monitor")


    def test_add_incorrect_product_to_cart(self):
        """Check if responds correctly to adding a non-existent product to Cart"""

        out = cart.add_product_to_cart(7, "Czekolada")

        self.assertFalse(out)

    def test_add_duplicate_product_to_cart(self):
        """Check if responds correctly to adding a duplicate product to Cart"""

        out = cart.add_product_to_cart(7, "Telewizor")

        self.assertFalse(out)

    def test_add_product_to_empty_cart(self):
        """Check if responds correctly to adding a product to non-existent Cart"""

        product.add_product("Monitor", "Opis monitora", 777.77)
        out = cart.add_product_to_cart(7, 4, 2)

        self.assertFalse(out)

    def test_remove_product_from_cart(self):
        """Check if correctly removes product from Cart"""

        out = cart.remove_product_from_cart(1)
        prod, amount = cart.get_product_from_cart(1)

        self.assertTrue(out)
        self.assertEqual(amount, 0)
        self.assertIsNone(prod)

    def test_remove_incorrect_product_from_cart(self):
        """Check if responds correctly to removing a non-existent product from Cart"""

        out = cart.remove_product_from_cart(100)

        self.assertFalse(out)

    def test_remove_product_from_empty_cart(self):
        """Check if responds correctly to removing a product from non-existent Cart"""

        out = cart.remove_product_from_cart(1, 100)

        self.assertFalse(out)
