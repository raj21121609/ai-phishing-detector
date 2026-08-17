from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AnalyzeEmailTests(APITestCase):
    def setUp(self):
        self.url = reverse('analyze-email')

    def test_analyze_email_success(self):
        data = {"email_text": "This is a test email"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('metadata', response.data)
        self.assertIn('sender', response.data)
        self.assertIn('text_signals', response.data)
        self.assertIn('urls', response.data)

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
