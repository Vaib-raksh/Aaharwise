from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.database.database import create_tables
from backend.nutrition.food_db import search_foods
from backend.nutrition.nutrition_engine import get_food_nutrition
from backend.services.health_service import calculate_bmi, estimate_daily_energy
from backend.timeline.evidence import DEFAULT_EVIDENCE
from backend.timeline.timeline_engine import generate_timeline


app = FastAPI(title="AaharWise API", version="0.1.0")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.on_event("startup")
def initialize_database() -> None:
	create_tables()


@app.get("/health")
def health_check() -> dict[str, str]:
	return {"status": "ok"}


@app.get("/api/foods/search")
def food_search(
	q: str = Query(min_length=1, description="Food name or partial name"),
	limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, list[dict[str, Any]]]:
	try:
		return {"foods": search_foods(q, limit)}
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/nutrition")
def nutrition_lookup(
	food: str = Query(min_length=1),
	quantity_g: float = Query(default=100, gt=0),
) -> dict[str, Any]:
	try:
		result = get_food_nutrition(food, quantity_g)
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc)) from exc

	if result is None:
		raise HTTPException(status_code=404, detail=f"Food not found: {food}")
	return result


@app.get("/api/health/estimate")
def health_estimate(
	age_years: float = Query(gt=0),
	weight_kg: float = Query(gt=0),
	height_cm: float = Query(gt=0),
	activity_factor: float = Query(default=1.2, gt=0),
) -> dict[str, Any]:
	try:
		return {
			"bmi": calculate_bmi(weight_kg, height_cm),
			"estimated_daily_energy_kj": estimate_daily_energy(
				age_years, weight_kg, height_cm, activity_factor
			),
			"is_estimate": True,
		}
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/timeline")
def nutrition_timeline(
	protein_g: float = Query(default=0, ge=0),
	fiber_g: float = Query(default=0, ge=0),
) -> dict[str, Any]:
	return {
		"timeline": generate_timeline(
			{"protein_g": protein_g, "fiber_g": fiber_g}, DEFAULT_EVIDENCE
		),
		"is_prediction": False,
	}
