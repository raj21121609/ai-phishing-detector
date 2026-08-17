from rest_framework import serializers
from .models import AnalysisRecord

class EmailAnalyzeSerializer(serializers.Serializer):
    email_text = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100000,
        error_messages={
            'blank': 'Email text cannot be empty.',
            'max_length': 'Email text is too large. Maximum size is 100,000 characters.'
        }
    )

class AnalysisRecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisRecord
        fields = ['id', 'created_at', 'sender', 'subject', 'risk_score', 'risk_level', 'phishing_probability', 'detected_threat_count']

class AnalysisRecordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisRecord
        fields = '__all__'
