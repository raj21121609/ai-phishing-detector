from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailAnalyzeSerializer
from .pipeline.orchestrator import analyze_email_content

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
            
            return Response(analysis_results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
