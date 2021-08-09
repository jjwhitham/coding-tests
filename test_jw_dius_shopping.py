import unittest
from decimal import Decimal
from jw_dius_shopping import PricingRules, Checkout


class CorrectTotals(unittest.TestCase):
    def setUp(self):
        self.pricing_rules = PricingRules()

    def test_correct_total_1(self):
        """SKUs Scanned: atv, atv, atv, vga Total expected: $249.00"""
        co = Checkout(self.pricing_rules)
        skus = ["atv", "atv", "atv", "vga"]
        for sku in skus:
            co.scan(sku)
        self.assertEqual(co.total(), Decimal("249.00"))

    def test_correct_total_2(self):
        """SKUs Scanned: atv, ipd, ipd, atv, ipd, ipd, ipd Total expected: $2718.95"""
        co = Checkout(self.pricing_rules)
        skus = ["atv", "ipd", "ipd", "atv", "ipd", "ipd", "ipd"]
        for sku in skus:
            co.scan(sku)
        self.assertEqual(co.total(), Decimal("2718.95"))

    def test_correct_total_3(self):
        """SKUs Scanned: mbp, vga, ipd Total expected: $1949.98"""
        co = Checkout(self.pricing_rules)
        skus = ["mbp", "vga", "ipd"]
        for sku in skus:
            co.scan(sku)
        self.assertEqual(co.total(), Decimal("1949.98"))


if __name__ == "__main__":

    unittest.main()
