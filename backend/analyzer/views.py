from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailAnalyzeSerializer

class AnalyzeEmailView(APIView):
    def post(self, request):
        serializer = EmailAnalyzeSerializer(data=request.data)
        if serializer.is_valid():
            email_text = serializer.validated_data['email_text']
            return Response({
                "message": "Email received successfully",
                "length": len(email_text)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
