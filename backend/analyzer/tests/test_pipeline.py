import os
from django.test import TestCase
from analyzer.pipeline.email_parser import parse_email
from analyzer.pipeline.text_analyzer import analyze_text
from analyzer.pipeline.url_extractor import extract_and_analyze_urls
from analyzer.pipeline.sender_analyzer import analyze_sender
from analyzer.pipeline.orchestrator import analyze_email_content

class PipelineTests(TestCase):
    
    def test_email_parser_raw_text(self):
        text = "This is just a raw body with no headers."
        parsed = parse_email(text)
        self.assertIsNone(parsed['sender'])
        self.assertEqual(parsed['body'], text)
        
    def test_email_parser_with_headers(self):
        text = "From: test@example.com\nTo: victim@example.com\nSubject: Urgent\n\nPlease click."
        parsed = parse_email(text)
        self.assertEqual(parsed['sender'], "test@example.com")
        self.assertEqual(parsed['subject'], "Urgent")
        self.assertEqual(parsed['body'], "Please click.")
        
    def test_text_analyzer(self):
        body = "You must act now to update your password before we close your account."
        signals = analyze_text(body, "Action Required")
        self.assertIn("urgency", signals)
        self.assertIn("password_request", signals)
        self.assertIn("threats", signals)
        
    def test_url_extractor(self):
        text = "Check this link: http://192.168.1.1/login.php and https://bit.ly/123 and https://micros0ft.com"
        urls = extract_and_analyze_urls(text)
        self.assertEqual(len(urls), 3)
        
        ip_url = next(u for u in urls if '192.168.1.1' in u['url'])
        self.assertTrue(ip_url['features']['has_ip'])
        self.assertFalse(ip_url['features']['https_usage'])
        self.assertIn('login', ip_url['features']['suspicious_keywords'])
        self.assertGreater(ip_url['risk_score'], 50)
        
        short_url = next(u for u in urls if 'bit.ly' in u['url'])
        self.assertTrue(short_url['features']['is_shortened'])
        self.assertTrue(short_url['features']['https_usage'])
        
        typo_url = next(u for u in urls if 'micros0ft' in u['url'])
        self.assertEqual(typo_url['features']['impersonated_brand'], 'microsoft')
        self.assertIn("Possible brand impersonation of 'microsoft'", typo_url['signals'])
        self.assertGreaterEqual(typo_url['risk_score'], 50)
        
    def test_sender_analyzer(self):
        sender = "Support Team <support@gmail.com>"
        reply_to = "hacker@evil.com"
        result = analyze_sender(sender, reply_to)
        
        self.assertEqual(result['sender_email'], "support@gmail.com")
        self.assertTrue(result['is_free_provider'])
        self.assertTrue(result['reply_to_mismatch'])
        
    def test_orchestrator(self):
        text = "From: admin@paypal.com\nSubject: Verify your account\n\nPlease login here: http://bit.ly/xyz to verify."
        result = analyze_email_content(text)
        
        self.assertEqual(result['metadata']['subject'], "Verify your account")
        self.assertEqual(result['sender']['sender_domain'], "paypal.com")
        self.assertIn("password_request", result['text_signals'])
        self.assertEqual(len(result['urls']), 1)
        self.assertTrue(result['urls'][0]['features']['is_shortened'])
