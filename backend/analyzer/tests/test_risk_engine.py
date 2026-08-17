from django.test import TestCase
from analyzer.pipeline.risk_engine import calculate_risk_score

class RiskEngineTests(TestCase):
    
    def test_legitimate_email(self):
        ml_data = {"probability": 0.1}
        text_signals = []
        url_data = []
        sender_data = {"reply_to_mismatch": False, "suspicious_domain_structure": False, "is_free_provider": False}
        
        result = calculate_risk_score(ml_data, text_signals, url_data, sender_data)
        self.assertEqual(result["risk_level"], "LOW")
        self.assertLess(result["risk_score"], 30)
        
    def test_phishing_email(self):
        ml_data = {"probability": 0.95}
        text_signals = ["urgency", "credential_request"]
        url_data = [{"risk_score": 90, "signals": ["Suspicious keyword"]}]
        sender_data = {"reply_to_mismatch": True}
        
        result = calculate_risk_score(ml_data, text_signals, url_data, sender_data)
        self.assertEqual(result["risk_level"], "CRITICAL")
        self.assertGreaterEqual(result["risk_score"], 80)
        
    def test_ambiguous_email(self):
        ml_data = {"probability": 0.55}
        text_signals = ["urgency", "payment_request"]
        url_data = []
        sender_data = {"is_free_provider": True}
        
        result = calculate_risk_score(ml_data, text_signals, url_data, sender_data)
        self.assertEqual(result["risk_level"], "MEDIUM")
        
    def test_suspicious_url(self):
        ml_data = {"probability": 0.2}
        text_signals = []
        url_data = [{"risk_score": 100, "signals": ["Brand impersonation"]}]
        sender_data = {}
        
        result = calculate_risk_score(ml_data, text_signals, url_data, sender_data)
        self.assertIn("Brand impersonation", result["detected_threats"])
        self.assertGreaterEqual(result["risk_score"], 30)
        
    def test_suspicious_sender(self):
        ml_data = {"probability": 0.1}
        text_signals = []
        url_data = []
        sender_data = {"reply_to_mismatch": True, "suspicious_domain_structure": True}
        
        result = calculate_risk_score(ml_data, text_signals, url_data, sender_data)
        self.assertIn("Sender and Reply-To addresses do not match", result["detected_threats"])
