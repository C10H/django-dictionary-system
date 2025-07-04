from django.db import models
from django.contrib.auth.models import User

class DictionaryEntry(models.Model):
    word = models.CharField(max_length=200, unique=True)
    translation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.word} - {self.translation}"
    
    class Meta:
        verbose_name_plural = "Dictionary Entries"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
