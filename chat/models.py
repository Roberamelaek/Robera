from django.db import models
import uuid
from django.utils import timezone

class TextToSpeech(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    text = models.TextField()
    mp3_file = models.FileField(upload_to='mp3_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    mp3_count_today = models.PositiveIntegerField(default=0)
    last_generated_at = models.DateTimeField(null=True, blank=True)
    
    # Add a new field for user's IP address
    user_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"TextToSpeech object - ID: {self.user_id}"
