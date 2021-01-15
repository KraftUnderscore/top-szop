from django.test import TestCase
from server.database_operations import discount, product

class DiscountTestCase(TestCase):

    def setUp(self):
        product.add_product("Telewizor", "Opis telewizora", 1000.00)
        product.add_product("Laptop", "Opis laptopa", 2000.00)
        discount.add_discount("2021-01-20 00:00:01", "2021-01-27 23:59:59", 33.33, 500)
        discount.add_product_to_discount(1, 1)
        discount.add_product_to_discount(2, 1)

    def test_add_discount_incorrect_value(self):
        """Try adding incorrect Discount value"""

        out = discount.add_discount("2022-01-20 00:00:01", "2022-01-27 23:59:59", -50.21, 300)

        self.assertFalse(out)

    def test_add_discount_incorrect_cost(self):
        """Try adding incorrect Discount cost"""

        out = discount.add_discount("2022-01-20 00:00:01", "2022-01-27 23:59:59", 50.21, -300)

        self.assertFalse(out)

    def test_add_discount_incorrect_start_date(self):
        """Try adding incorrect Discount start_date"""

        out = discount.add_discount("calendar", "2022-01-27 23:59:59", 50.21, 300)

        self.assertFalse(out)

    def test_add_discount_incorrect_end_date(self):
        """Try adding incorrect Discount end_date"""

        out = discount.add_discount("2022-01-27 23:59:59", "telewizor", 50.21, 300)

        self.assertFalse(out)

    def test_add_discount_overlapping_start_date(self):
        """Try adding a new Discount, where its start_date is in the middle of
           another Discount's period"""

        out = discount.add_discount("2021-01-25 23:59:59", "2021-02-07 23:59:59", 50.21, 300)

        self.assertFalse(out)

    def test_add_discount_overlapping_end_date(self):
        """Try adding a new Discount, where its end_date is in the middle of
        another Discount's period"""

        out = discount.add_discount("2021-01-05 23:59:59", "2021-01-25 23:59:59", 50.21, 300)

        self.assertFalse(out)

    def test_add_discount_duration_in_other_discount(self):
        """Try adding a new Discount where its whole duration is inside another
           Discount's period"""

        out = discount.add_discount("2021-01-23 23:59:59", "2021-01-25 23:59:59", 50.21, 300)

        self.assertFalse(out)

    def test_add_discount_duration_covers_other_discount(self):
        """Try adding a new Discount where its duration is over duration of other Discount"""

        out = discount.add_discount("2021-01-05 23:59:59", "2021-02-25 23:59:59", 50.21, 300)

        self.assertFalse(out)

    def test_add_product_to_incorrect_discount(self):
        """Try adding a Product to a non-existent Discount"""

        out = discount.add_product_to_discount(1, 5)

        self.assertFalse(out)

    def test_add_incorrect_product_to_discount(self):
        """Try adding a non-existent Product to a Discount"""

        out = discount.add_product_to_discount(5, 1)

        self.assertFalse(out)

    def test_get_discount_data(self):
        """Try fetching data about existing Discount"""

        data = discount.get_discount_data(1)

        self.assertEqual(len(data['products']), 2)
        self.assertEqual(data['start_date'], discount.timezone_parse_date("2021-01-20 00:00:01"))
        self.assertEqual(data['end_date'], discount.timezone_parse_date("2021-01-27 23:59:59"))
        self.assertAlmostEqual(data['value'], 33.33)
        self.assertEqual(data['cost'], 500)

    def test_get_incorrect_discount_data(self):
        """Try fetching data about non-existing Discount"""

        data = discount.get_discount_data(5)

        self.assertIsNone(data)

    def test_get_discount_data_no_products(self):
        """Try fetching data about existing Discount without Products"""

        discount.add_discount("2022-10-10 10:00:00", "2022-11-12 10:00:00", 55.55, 1000)

        data = discount.get_discount_data(2)

        self.assertEqual(len(data['products']), 0)
        self.assertEqual(data['start_date'], discount.timezone_parse_date("2022-10-10 10:00:00"))
        self.assertEqual(data['end_date'], discount.timezone_parse_date("2022-11-12 10:00:00"))
        self.assertAlmostEqual(data['value'], 55.55)
        self.assertEqual(data['cost'], 1000)
