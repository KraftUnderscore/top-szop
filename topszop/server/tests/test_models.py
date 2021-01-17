from django.test import TestCase
from server.database_operations import *
from server.models import *

class ModelsTestCase(TestCase):

    def setUp(self):
        product.add_product("Produkt", "Opis", 123.45)
        cart.add_cart()
        cart.add_product_to_cart(2, "Produkt")
        order.add_order("admin@admin.com")
        discount.add_discount("2022-01-01 10:00:00", "2022-02-01 10:00:00", 50.00, 100)
        discount.add_product_to_discount(1, 1)
        Delivery.objects.create(order_id=1, delivery_data="ul. Legnicka 57, Wrocław")

    def test_str_fun(self):
        """Tests string representation of database models"""

        order = Order.objects.get(id__exact=1)

        self.assertEqual(str(Discount.objects.get(id__exact=1)), "2022-01-01 09:00:00+00:00 - 2022-02-01 09:00:00+00:00")
        self.assertEqual(str(Product.objects.get(id__exact=1)), "Produkt")
        self.assertEqual(str(Discount_Product.objects.get(discount_id__exact=1)), "Produkt 2022-01-01 09:00:00+00:00 - 2022-02-01 09:00:00+00:00")
        self.assertEqual(str(Cart_Product.objects.get(cart_id__exact=1)), "2 of Produkt")
        self.assertEqual(str(order), f"Order on {order.order_date} for 246.90")
        self.assertEqual(str(Delivery.objects.get(id__exact=1)), "Delivery: ul. Legnicka 57, Wrocław")
