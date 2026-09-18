import unittest

from fastapi.testclient import TestClient

from backend.main import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_food_search_uses_ifct_data(self):
        response = self.client.get("/api/foods/search", params={"q": "Bajra"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["foods"][0]["food_name"], "Bajra")

    def test_nutrition_endpoint_scales_quantity(self):
        response = self.client.get(
            "/api/nutrition", params={"food": "Bajra", "quantity_g": 50}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["energy_kj"], 728.0)

    def test_unknown_food_returns_not_found(self):
        response = self.client.get(
            "/api/nutrition", params={"food": "Food that is not in IFCT"}
        )

        self.assertEqual(response.status_code, 404)

    def test_health_estimate_is_labeled(self):
        response = self.client.get(
            "/api/health/estimate",
            params={"age_years": 30, "weight_kg": 70, "height_cm": 175},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_estimate"])

    def test_timeline_is_not_a_prediction(self):
        response = self.client.get(
            "/api/timeline", params={"protein_g": 15, "fiber_g": 8}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_prediction"])
        self.assertEqual(len(response.json()["timeline"]), 8)


if __name__ == "__main__":
    unittest.main()