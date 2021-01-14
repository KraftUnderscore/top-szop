from django.test import TestCase
from server.database_operations import product
from server.models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        product.add_product("Telewizor1", "Opis telewizora1", 1234.50)
        product.add_product("Telewizor2", "Opis telewizora2", 2345.60)
        product.add_product("Telewizor3", "Opis telewizora3", 3456.70)
        product.add_product("Pralka1", "Opis pralki1", 567.80)
        product.add_product("Pralka2", "Opis pralki2", 678.90)

    def test_add_product_duplicate_name(self):
        """Check if protect against adding duplicate Products"""

        output = product.add_product("Telewizor1", "Opis telewizora1", 1234.50)
        self.assertFalse(output)

    def test_remove_product(self):
        """Check if successfully removes product"""

        output = product.remove_product(1)
        prod = product.get_product_by_id(1)

        self.assertIsNone(prod)
        self.assertTrue(output)

    def test_remove_product_no_product_in_db(self):
        """Check if successfully removes product"""

        output = product.remove_product(10)

        self.assertFalse(output)

    def test_get_all_products(self):
        """Check if all products are correctly added and fetched"""
        products = product.get_all_products()

        self.assertEqual(len(products), 5)
        self.assertEqual(products[0].name, "Telewizor1")
        self.assertEqual(products[1].name, "Telewizor2")
        self.assertEqual(products[3].name, "Pralka1")
        self.assertEqual(products[4].name, "Pralka2")

    def test_get_all_products_none_in_db(self):
        """Check if returns empty list when no products in db"""

        Product.objects.all().delete()
        products = product.get_all_products()

        self.assertEqual(len(products), 0)

    def test_get_product_by_id(self):
        """Check if can get product by its id"""

        prod = product.get_product_by_id(3)

        self.assertEqual(prod.name, "Telewizor3")

    def test_get_product_by_id_no_match(self):
        """Check returns None when no match"""

        prod = product.get_product_by_id(100)

        self.assertIsNone(prod)

    def test_get_product_by_id_ivalid_id(self):
        """Check returns None when id is invalid"""

        prod = product.get_product_by_id(-1)

        self.assertIsNone(prod)

    def test_get_duplicate(self):
        """Check if can find similiar product"""

        prod = product.get_product_duplicate("Telewizor")

        self.assertEqual(prod.name, "Telewizor1")

    def test_get_duplicate_none_found(self):
        """Check if can find similiar product"""

        prod = product.get_product_duplicate("Kanapka")

        self.assertIsNone(prod)

    def test_get_products_from_search(self):
        """Check if can find all product from search"""

        prod_tvs = product.get_products_from_search("Telewizor")
        prod_wash = product.get_products_from_search("Pralka")

        self.assertEqual(len(prod_tvs), 3)
        self.assertEqual(len(prod_wash), 2)

    def test_get_products_from_search_none_found(self):
        """Check if can find all product from search"""

        prods = product.get_products_from_search("Kanapka")

        self.assertEqual(len(prods), 0)
