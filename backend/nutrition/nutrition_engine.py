from backend.database.database import get_connection


def get_food_nutrition(food_name, quantity_g=100):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT food_name, energy_kj, protein_g, fat_g,
               carbohydrate_g, fiber_g
        FROM foods
        WHERE food_name LIKE ?
        LIMIT 1
    """, (f"%{food_name}%",))

    food = cursor.fetchone()
    conn.close()

    if not food:
        return None

    name, energy, protein, fat, carbs, fiber = food

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