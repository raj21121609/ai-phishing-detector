import uuid
from django.db import models

class AnalysisRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    risk_score = models.IntegerField()
    risk_level = models.CharField(max_length=20)
    phishing_probability = models.FloatField()
    detected_threat_count = models.IntegerField()
    analysis_data = models.JSONField()
    
    class Meta:
        ordering = ['-created_at']
