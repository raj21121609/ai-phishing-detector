from django.urls import path
from .views import HealthCheckView
from analyzer.views import AnalyzeEmailView, AnalysisHistoryListView, AnalysisHistoryDetailView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('analyze/', AnalyzeEmailView.as_view(), name='analyze-email'),
    path('history/', AnalysisHistoryListView.as_view(), name='history-list'),
    path('history/<uuid:pk>/', AnalysisHistoryDetailView.as_view(), name='history-detail'),
]
