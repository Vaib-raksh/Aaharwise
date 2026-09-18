from numbers import Real

from backend.database.database import get_connection


def get_food_nutrition(food_name: str, quantity_g: Real = 100):
    """Return deterministic nutrition values scaled from the IFCT per-100 g data."""
    if not isinstance(food_name, str) or not food_name.strip():
        raise ValueError("food_name must be a non-empty string")

    if isinstance(quantity_g, bool) or not isinstance(quantity_g, Real):
        raise ValueError("quantity_g must be a positive number")

    if quantity_g <= 0:
        raise ValueError("quantity_g must be a positive number")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT food_name, energy_kj, protein_g, fat_g,
                   carbohydrate_g, fiber_g
            FROM foods
            WHERE food_name LIKE ?
            LIMIT 1
        """, (f"%{food_name.strip()}%",))

        food = cursor.fetchone()
    finally:
        conn.close()

    if not food:
        return None

    name, energy, protein, fat, carbs, fiber = food
    nutrients = (energy, protein, fat, carbs, fiber)
    if any(value is None for value in nutrients):
        raise ValueError(f"Nutrition data is incomplete for {name}")

    factor = quantity_g / 100

    return {
        "food": name,
        "quantity_g": quantity_g,
        "energy_kj": round(energy * factor, 2),
        "protein_g": round(protein * factor, 2),
        "fat_g": round(fat * factor, 2),
        "carbohydrate_g": round(carbs * factor, 2),
        "fiber_g": round(fiber * factor, 2)
    }


if __name__ == "__main__":
    result = get_food_nutrition("Bajra", 100)
    print(result)