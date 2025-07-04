import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionary_system.settings')
django.setup()

from django.contrib.auth.models import User
from dictionary.models import DictionaryEntry

def create_initial_data():
    if not DictionaryEntry.objects.exists():
        DictionaryEntry.objects.create(word="hello", translation="你好")
        DictionaryEntry.objects.create(word="test", translation="测试")
        DictionaryEntry.objects.create(word="时间", translation="time")
        print("Initial dictionary entries created")
    
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "password")
        print("Admin user created")

if __name__ == "__main__":
    create_initial_data()