from numbers import Real


def calculate_bmi(weight_kg: Real, height_cm: Real) -> float:
	"""Calculate BMI from metric measurements."""
	if isinstance(weight_kg, bool) or isinstance(height_cm, bool):
		raise ValueError("weight and height must be positive numbers")
	if not isinstance(weight_kg, Real) or not isinstance(height_cm, Real):
		raise ValueError("weight and height must be positive numbers")
	if weight_kg <= 0 or height_cm <= 0:
		raise ValueError("weight and height must be positive numbers")

	height_m = height_cm / 100
	return round(weight_kg / (height_m * height_m), 2)


def estimate_daily_energy(
	age_years: Real,
	weight_kg: Real,
	height_cm: Real,
	activity_factor: Real = 1.2,
) -> float:
	"""Estimate daily energy needs with Mifflin-St Jeor's sex-neutral baseline.

	This is an estimate for education and planning, not a medical prescription.
	"""
	values = (age_years, weight_kg, height_cm, activity_factor)
	if any(isinstance(value, bool) or not isinstance(value, Real) for value in values):
		raise ValueError("health measurements must be numbers")
	if age_years <= 0 or weight_kg <= 0 or height_cm <= 0 or activity_factor <= 0:
		raise ValueError("health measurements must be positive")

	resting_energy = 10 * weight_kg + 6.25 * height_cm - 5 * age_years
	return round(resting_energy * activity_factor, 2)
