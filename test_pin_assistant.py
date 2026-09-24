import unittest
from pin_assistant import validate_pin, get_provider_info, PROVIDERS

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

    def test_get_provider_info(self):
        kamu = get_provider_info("kamusm")
        self.assertIsNotNone(kamu)
        self.assertIn("Kamu SM", kamu["name"])

        invalid = get_provider_info("nonexistent")
        self.assertIsNone(invalid)

if __name__ == "__main__":
    unittest.main()
