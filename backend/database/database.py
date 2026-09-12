import sqlite3
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Database location
DB_PATH = BASE_DIR / "backend" / "database" / "aaharwise_v2.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ifct_code TEXT UNIQUE NOT NULL,
            food_name TEXT NOT NULL,
            scientific_name TEXT,
            food_group TEXT,
            tags TEXT,

            energy_kj REAL,
            water_g REAL,
            protein_g REAL,
            fat_g REAL,
            carbohydrate_g REAL,
            fiber_g REAL,

            calcium_g REAL,
            iron_g REAL,
            magnesium_g REAL,
            phosphorus_g REAL,
            potassium_g REAL,
            sodium_g REAL,
            zinc_g REAL,

            vitamin_a REAL,
            vitamin_c REAL,
            vitamin_d REAL,
            vitamin_e REAL,
            vitamin_k REAL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("AaharWise v2 database created successfully.")