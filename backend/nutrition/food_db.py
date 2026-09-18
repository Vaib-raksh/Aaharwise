from typing import Any

from backend.database.database import get_connection


def search_foods(query: str, limit: int = 20) -> list[dict[str, Any]]:
	"""Search the read-only IFCT food catalog by name."""
	normalized_query = query.strip()
	if not normalized_query:
		raise ValueError("query must be a non-empty string")
	if limit < 1 or limit > 100:
		raise ValueError("limit must be between 1 and 100")

	conn = get_connection()
	try:
		rows = conn.execute(
			"""
			SELECT ifct_code, food_name, food_group
			FROM foods
			WHERE food_name LIKE ?
			ORDER BY food_name
			LIMIT ?
			""",
			(f"%{normalized_query}%", limit),
		).fetchall()
	finally:
		conn.close()

	return [
		{"ifct_code": code, "food_name": name, "food_group": group}
		for code, name, group in rows
	]
