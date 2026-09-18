import unittest

from backend.nutrition.nutrition_engine import get_food_nutrition


class NutritionEngineTests(unittest.TestCase):
    def test_bajra_nutrition_at_100_grams(self):
        result = get_food_nutrition("Bajra", 100)

        self.assertEqual(result, {
            "food": "Bajra",
            "quantity_g": 100,
            "energy_kj": 1456.0,
            "protein_g": 10.96,
            "fat_g": 5.43,
            "carbohydrate_g": 61.78,
            "fiber_g": 11.49,
        })

    def test_bajra_nutrition_scales_to_50_grams(self):
        result = get_food_nutrition("Bajra", 50)

        self.assertEqual(result["quantity_g"], 50)
        self.assertEqual(result["energy_kj"], 728.0)
        self.assertEqual(result["protein_g"], 5.48)
        self.assertEqual(result["fiber_g"], 5.75)

    def test_unknown_food_returns_none(self):
        self.assertIsNone(get_food_nutrition("Food that is not in IFCT"))

    def test_invalid_quantity_is_rejected(self):
        for quantity in (0, -10, True, "100"):
            with self.subTest(quantity=quantity):
                with self.assertRaisesRegex(ValueError, "positive number"):
                    get_food_nutrition("Bajra", quantity)

    def test_blank_food_name_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-empty string"):
            get_food_nutrition("   ")