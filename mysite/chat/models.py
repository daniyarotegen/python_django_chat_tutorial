from django.db import models
from django.utils import timezone


class ChatMessage(models.Model):
    room_name = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']
