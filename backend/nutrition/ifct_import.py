import csv
from pathlib import Path
import sys

# Allow importing database.py
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from backend.database.database import get_connection


CSV_PATH = BASE_DIR / "data" / "ifct" / "compositions.csv"


def import_ifct_data():
    conn = get_connection()
    cursor = conn.cursor()

    with open(CSV_PATH, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        count = 0

        for row in reader:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO foods (
                        ifct_code,
                        food_name,
                        scientific_name,
                        food_group,
                        tags,
                        energy_kj,
                        water_g,
                        protein_g,
                        fat_g,
                        carbohydrate_g,
                        fiber_g
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row.get("code"),
                    row.get("name"),
                    row.get("scie"),
                    row.get("grup"),
                    row.get("tags"),
                    float(row.get("enerc") or 0),
                    float(row.get("water") or 0),
                    float(row.get("protcnt") or 0),
                    float(row.get("fatce") or 0),
                    float(row.get("choavldf") or 0),
                    float(row.get("fibtg") or 0)
                ))

                count += 1

            except (ValueError, TypeError):
                continue

    conn.commit()
    conn.close()

    print(f"Imported {count} food records.")


if __name__ == "__main__":
    import_ifct_data()