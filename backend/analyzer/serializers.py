from rest_framework import serializers

class EmailAnalyzeSerializer(serializers.Serializer):
    email_text = serializers.CharField(required=True, allow_blank=False)
