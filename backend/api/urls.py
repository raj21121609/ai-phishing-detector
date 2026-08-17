from django.urls import path
from .views import HealthCheckView
from analyzer.views import AnalyzeEmailView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('analyze/', AnalyzeEmailView.as_view(), name='analyze-email'),
]
