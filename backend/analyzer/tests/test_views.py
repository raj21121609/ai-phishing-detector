from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AnalyzeEmailTests(APITestCase):
    def setUp(self):
        self.url = reverse('analyze-email')

    def test_analyze_email_success(self):
        data = {"email_text": "This is a test email"}
        response = self.client.post(self.url, data, format='json')
        self.assertIn('risk_score', response.data)
        self.assertIn('risk_level', response.data)
        self.assertIn('ml_probability', response.data)
        self.assertIn('detected_threats', response.data)
        self.assertIn('explanation', response.data)
        self.assertIn('details', response.data)

    def test_analyze_email_empty(self):
        data = {"email_text": ""}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email_text", response.data)

    def test_analyze_email_missing(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email_text", response.data)
