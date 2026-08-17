from django.test import TestCase
from analyzer.pipeline.explainer import generate_explanation

class ExplainerTests(TestCase):
    def test_explainer_clean(self):
        details = {"urls": [], "sender": {}, "text_signals": []}
        result = generate_explanation("LOW", 10, 0.1, details)
        self.assertEqual(len(result["reasons"]), 0)
        self.assertIn("No significant threats", result["summary"])
        
    def test_explainer_critical(self):
        details = {
            "urls": [{"features": {"impersonated_brand": "paypal"}}],
            "sender": {"reply_to_mismatch": True},
            "text_signals": ["urgency", "credential_request"]
        }
        result = generate_explanation("CRITICAL", 95, 0.9, details)
        self.assertGreaterEqual(len(result["reasons"]), 2)
        
        categories = [r["category"] for r in result["reasons"]]
        self.assertIn("MACHINE_LEARNING", categories)
        self.assertIn("URL", categories)
        self.assertIn("SOCIAL_ENGINEERING", categories)
        self.assertIn("SENDER", categories)
