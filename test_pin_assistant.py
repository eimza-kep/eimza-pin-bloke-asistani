import unittest
from pin_assistant import (
    validate_pin,
    validate_puk,
    get_provider_info,
    generate_secure_pin,
    generate_puk_unblock_apdu,
    generate_html_guide,
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

    def test_validate_puk_valid(self):
        res = validate_puk("12345678")
        self.assertTrue(res["valid"])

        res_alpha = validate_puk("A1B2C3D4")
        self.assertTrue(res_alpha["valid"])

    def test_validate_puk_invalid_length(self):
        res_short = validate_puk("12345")
        self.assertFalse(res_short["valid"])
        self.assertIn("8 karakter", res_short["reason"])

        res_long = validate_puk("123456789")
        self.assertFalse(res_long["valid"])

    def test_validate_puk_invalid_chars(self):
        res_chars = validate_puk("1234-567")
        self.assertFalse(res_chars["valid"])
        self.assertIn("harf ve rakam", res_chars["reason"])

    def test_validate_puk_all_same(self):
        res_same = validate_puk("00000000")
        self.assertFalse(res_same["valid"])

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

        # Test invalid PUK in APDU
        with self.assertRaises(ValueError):
            generate_puk_unblock_apdu("akis", "123", "482915")

    def test_generate_html_guide(self):
        html = generate_html_guide()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("TÜBİTAK Kamu SM", html)
        self.assertIn("TÜRKTRUST", html)
        self.assertIn("v1.3", html)

if __name__ == "__main__":
    unittest.main()
