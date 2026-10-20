import unittest
from pin_assistant import (
    validate_pin,
    get_provider_info,
    generate_secure_pin,
    generate_puk_unblock_apdu,
    PROVIDERS
)

class TestPinAssistant(unittest.TestCase):
    def test_validate_pin_valid(self):
        res = validate_pin("482915")
        self.assertTrue(res["valid"])

        res8 = validate_pin("93710528")
        self.assertTrue(res8["valid"])

    def test_validate_pin_too_short(self):
        res = validate_pin("1234")
        self.assertFalse(res["valid"])
        self.assertIn("6-8 basamak", res["reason"])

    def test_validate_pin_too_long(self):
        res = validate_pin("123456789")
        self.assertFalse(res["valid"])

    def test_validate_pin_non_digits(self):
        res = validate_pin("12a456")
        self.assertFalse(res["valid"])
        self.assertIn("rakamlardan", res["reason"])

    def test_validate_pin_all_same(self):
        res = validate_pin("222222")
        self.assertFalse(res["valid"])
        self.assertIn("aynı olan", res["reason"])

    def test_validate_pin_sequential(self):
        res1 = validate_pin("123456")
        self.assertFalse(res1["valid"])
        self.assertIn("artan", res1["reason"])

        res2 = validate_pin("654321")
        self.assertFalse(res2["valid"])
        self.assertIn("azalan", res2["reason"])

    def test_generate_secure_pin(self):
        for _ in range(5):
            pin = generate_secure_pin(6)
            self.assertEqual(len(pin), 6)
            self.assertTrue(validate_pin(pin)["valid"])

    def test_get_provider_info(self):
        kamu = get_provider_info("kamusm")
        self.assertIsNotNone(kamu)
        self.assertIn("Kamu SM", kamu["name"])

        edm = get_provider_info("edmbilisim")
        self.assertIsNotNone(edm)
        self.assertIn("EDM", edm["name"])

        invalid = get_provider_info("nonexistent")
        self.assertIsNone(invalid)

    def test_generate_puk_unblock_apdu(self):
        # Test AKIS APDU
        res_akis = generate_puk_unblock_apdu("akis", "12345678", "482915")
        self.assertEqual(res_akis["card_type"], "akis")
        self.assertTrue(res_akis["apdu_hex"].startswith("00 2C 02 81 10"))
        self.assertIn("AKİS", res_akis["explanation"])
        self.assertIn("90 00", res_akis["expected_response"])

        # Test CardOS APDU
        res_cardos = generate_puk_unblock_apdu("cardos", "87654321", "593812")
        self.assertEqual(res_cardos["card_type"], "cardos")
        self.assertTrue(res_cardos["apdu_hex"].startswith("00 2C 00 01 10"))
        self.assertIn("CardOS", res_cardos["explanation"])

        # Test invalid PIN in APDU
        with self.assertRaises(ValueError):
            generate_puk_unblock_apdu("akis", "12345678", "123456")

if __name__ == "__main__":
    unittest.main()
