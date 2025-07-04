from django.contrib import admin
from .models import DictionaryEntry, UserProfile

@admin.register(DictionaryEntry)
class DictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation', 'created_at', 'updated_at']
    search_fields = ['word', 'translation']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-updated_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
