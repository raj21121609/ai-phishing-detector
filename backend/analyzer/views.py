from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from .serializers import EmailAnalyzeSerializer, AnalysisRecordListSerializer, AnalysisRecordDetailSerializer
from .pipeline.orchestrator import analyze_email_content
from .models import AnalysisRecord

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "phishguard-api"}, status=status.HTTP_200_OK)

class AnalyzeEmailView(APIView):
    def post(self, request):
        serializer = EmailAnalyzeSerializer(data=request.data)
        if serializer.is_valid():
            email_text = serializer.validated_data['email_text']
            
            analysis_results = analyze_email_content(email_text)
            
            if "error" in analysis_results:
                return Response(
                    {"error": "Analysis failed", "message": "An unexpected error occurred during processing."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            try:
                email_meta = analysis_results.get("email", {})
                AnalysisRecord.objects.create(
                    sender=email_meta.get("sender") or "Unknown",
                    subject=email_meta.get("subject") or "No Subject",
                    risk_score=analysis_results.get("risk_score", 0),
                    risk_level=analysis_results.get("risk_level", "LOW"),
                    phishing_probability=analysis_results.get("phishing_probability", 0.0),
                    detected_threat_count=len(analysis_results.get("threats", [])),
                    analysis_data=analysis_results
                )
            except Exception:
                pass
            
            return Response(analysis_results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AnalysisHistoryListView(generics.ListAPIView):
    queryset = AnalysisRecord.objects.all()
    serializer_class = AnalysisRecordListSerializer
    pagination_class = StandardResultsSetPagination

class AnalysisHistoryDetailView(generics.RetrieveAPIView):
    queryset = AnalysisRecord.objects.all()
    serializer_class = AnalysisRecordDetailSerializer
