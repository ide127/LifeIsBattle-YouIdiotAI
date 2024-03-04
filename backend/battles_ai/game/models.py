from datetime import timezone
from django.db import models
import uuid
from django.utils import timezone
from openai import OpenAI

class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    OpenAI_thread_id = models.CharField(max_length=127, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_successful = models.BooleanField(null=True, default=None)
    user_ip = models.CharField(max_length=15)
    user_language = models.CharField(max_length=5, default='EN')
    
    def __str__(self):
        return f'ID: {self.id} - start: {self.start_time} - end: {self.end_time}'

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'ID: {self.id} - text: {self.text[:50]}...'
        

class Leaderboard(models.Model):
    nickname = models.CharField(max_length=30, unique=True)
    score = models.DecimalField(max_digits=10, decimal_places=5)
    num_str = models.IntegerField()
    language = models.CharField(max_length=5)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='leaderboard_entry')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nickname}: {self.score}"
    
    class Meta:
        ordering = ['-score', 'timestamp']
