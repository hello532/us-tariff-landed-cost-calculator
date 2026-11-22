import unittest
from tariff_calc import calculate_tariff_reprice, calculate_multichannel_payout


class TestTariffAndMultiChannel(unittest.TestCase):
    def test_500_unit_stacked_tariff_example(self):
        res = calculate_tariff_reprice()
        self.assertEqual(res["customs_value"], 3400.00)
        self.assertEqual(res["stacked_duty_rate_pct"], 51.5)
        self.assertEqual(res["mpf_total"], 31.67)
        self.assertEqual(res["landed_per_unit"], 12.50)
        self.assertEqual(res["profit_preserving_price"], 33.03)
        self.assertEqual(res["target_margin_reprice"], 33.79)

    def test_38_sku_tiktok_vs_shopify_example(self):
        res = calculate_multichannel_payout()
        self.assertEqual(res["realized_sale"], 34.20)
        self.assertEqual(res["shopify_net"], 19.71)
        self.assertEqual(res["tiktok_net"], 12.32)
        self.assertEqual(res["payout_spread"], 7.39)
        self.assertEqual(res["max_affiliate_pct"], 16.02)
        self.assertEqual(res["tiktok_target_list"], 37.13)


if __name__ == "__main__":
    unittest.main()
