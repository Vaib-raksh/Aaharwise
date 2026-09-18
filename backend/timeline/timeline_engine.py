from typing import Any

from backend.timeline.timeline_rules import TIMELINE_STAGES, classify_pattern


def generate_timeline(nutrition: dict[str, float], evidence: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
	"""Generate cautious timeline statements from a deterministic nutrition summary."""
	pattern = classify_pattern(nutrition)
	evidence_items = evidence or []
	return [
		{
			"stage": stage,
			"pattern": pattern,
			"mechanism": mechanism,
			"implication": implication,
			"evidence": evidence_items,
		}
		for stage, mechanism, implication in TIMELINE_STAGES
	]
