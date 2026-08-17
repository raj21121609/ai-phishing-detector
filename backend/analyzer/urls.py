from django.urls import path
from .views import HealthCheckView, AnalyzeEmailView, AnalysisHistoryListView, AnalysisHistoryDetailView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('analyze/', AnalyzeEmailView.as_view(), name='analyze_email'),
    path('history/', AnalysisHistoryListView.as_view(), name='analysis_history_list'),
    path('history/<uuid:pk>/', AnalysisHistoryDetailView.as_view(), name='analysis_history_detail'),
]
