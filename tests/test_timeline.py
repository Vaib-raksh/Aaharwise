import unittest

from backend.timeline.timeline_engine import generate_timeline
from backend.timeline.timeline_rules import classify_pattern


class TimelineTests(unittest.TestCase):
    def test_high_fiber_protein_pattern_is_classified(self):
        self.assertEqual(
            classify_pattern({"fiber_g": 8, "protein_g": 15}),
            "higher-fiber and protein-containing",
        )

    def test_timeline_has_all_long_term_stages(self):
        timeline = generate_timeline({"fiber_g": 8, "protein_g": 15})

        self.assertEqual(len(timeline), 8)
        self.assertEqual(timeline[0]["stage"], "today")
        self.assertEqual(timeline[-1]["stage"], "40 years")
        implications = " ".join(item["implication"] for item in timeline).lower()
        self.assertNotIn("will cause", implications)
        self.assertNotIn("guaranteed", implications)

    def test_timeline_accepts_identifiable_evidence(self):
        evidence = [{"source": "Test source", "claim": "Test claim"}]

        self.assertEqual(generate_timeline({}, evidence)[0]["evidence"], evidence)


if __name__ == "__main__":
    unittest.main()