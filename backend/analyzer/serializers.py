from rest_framework import serializers

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
