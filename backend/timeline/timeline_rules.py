TIMELINE_STAGES = (
	("today", "Current meal", "Single-meal exposure is recorded without projecting disease outcomes."),
	("weeks", "Repeated weekly pattern", "Repeated choices can shape average intake and meal consistency."),
	("months", "Sustained pattern", "Persisting nutrient balance may influence body-weight and metabolic trends."),
	("years", "Long-term pattern", "A frequent pattern may contribute to cardiometabolic risk over time."),
	("10 years", "Decade-scale exposure", "Risk associations become more relevant if the pattern remains frequent."),
	("20 years", "Multi-decade exposure", "Cumulative dietary context may be associated with long-term health risk."),
	("30 years", "Extended exposure", "Long-running patterns can compound with activity, sleep, and genetics."),
	("40 years", "Life-course pattern", "This is a cautious association, not a deterministic prediction or diagnosis."),
)


def classify_pattern(nutrition: dict[str, float]) -> str:
	"""Classify a meal pattern using transparent, non-diagnostic rules."""
	fiber = nutrition.get("fiber_g", 0)
	protein = nutrition.get("protein_g", 0)
	return "higher-fiber and protein-containing" if fiber >= 5 and protein >= 10 else "mixed nutrient pattern"
