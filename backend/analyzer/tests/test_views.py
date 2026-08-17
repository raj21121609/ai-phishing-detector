from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from analyzer.models import AnalysisRecord

class AnalyzeEmailViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('analyze-email')

    def test_analyze_email_success(self):
        data = {"email_text": "This is a test email from fake@paypal.com asking for your password."}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('risk_score', response.data)
        self.assertIn('risk_level', response.data)
        self.assertIn('phishing_probability', response.data)
        self.assertIn('email', response.data)
        self.assertIn('threats', response.data)
        self.assertIn('url_analysis', response.data)
        self.assertIn('explanation', response.data)
        
        self.assertEqual(AnalysisRecord.objects.count(), 1)

    def test_analyze_email_empty(self):
        data = {"email_text": ""}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email text cannot be empty", str(response.data))

    def test_analyze_email_too_large(self):
        data = {"email_text": "A" * 100001}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email text is too large", str(response.data))

    def test_analyze_email_missing(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AnalysisHistoryTests(APITestCase):
    def setUp(self):
        self.list_url = reverse('history-list')
        self.record = AnalysisRecord.objects.create(
            sender="test@test.com",
            subject="Test Subject",
            risk_score=50,
            risk_level="MEDIUM",
            phishing_probability=0.5,
            detected_threat_count=1,
            analysis_data={"test": "data"}
        )
        self.detail_url = reverse('history-detail', args=[self.record.id])

    def test_history_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertNotIn('analysis_data', response.data['results'][0])
        self.assertEqual(response.data['results'][0]['subject'], "Test Subject")
        
    def test_history_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('analysis_data', response.data)
        self.assertEqual(response.data['analysis_data']['test'], "data")
