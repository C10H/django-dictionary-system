from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import DictionaryEntry
import json
import re
import requests
import hashlib
import random
import time

def home(request):
    return render(request, 'dictionary/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_panel')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'dictionary/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'dictionary/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'dictionary/register.html')
        
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Registration successful')
        return redirect('login')
    
    return render(request, 'dictionary/register.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def admin_panel(request):
    entries = DictionaryEntry.objects.all().order_by('-updated_at')
    return render(request, 'dictionary/admin_panel.html', {'entries': entries})

@login_required
@require_http_methods(["POST"])
def add_entry(request):
    word = request.POST.get('word', '').strip()
    translation = request.POST.get('translation', '').strip()
    
    if word and translation:
        entry, created = DictionaryEntry.objects.get_or_create(
            word=word,
            defaults={'translation': translation}
        )
        if not created:
            entry.translation = translation
            entry.save()
            messages.success(request, f'Entry "{word}" updated successfully')
        else:
            messages.success(request, f'Entry "{word}" added successfully')
    else:
        messages.error(request, 'Both word and translation are required')
    
    return redirect('admin_panel')

@login_required
@require_http_methods(["POST"])
def delete_entry(request, entry_id):
    try:
        entry = DictionaryEntry.objects.get(id=entry_id)
        word = entry.word
        entry.delete()
        messages.success(request, f'Entry "{word}" deleted successfully')
    except DictionaryEntry.DoesNotExist:
        messages.error(request, 'Entry not found')
    
    return redirect('admin_panel')

def is_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def baidu_translate(text, from_lang='auto', to_lang='en'):
    app_id = '20240531002066782'
    secret_key = '2UYrEDwvtMgOShDLo3u8'
    
    salt = str(random.randint(32768, 65536))
    sign_str = app_id + text + salt + secret_key
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    params = {
        'q': text,
        'from': from_lang,
        'to': to_lang,
        'appid': app_id,
        'salt': salt,
        'sign': sign
    }
    
    try:
        response = requests.get(url, params=params)
        result = response.json()
        if 'trans_result' in result:
            return result['trans_result'][0]['dst']
        return None
    except:
        return None

@csrf_exempt
@require_http_methods(["POST"])
def translate(request):
    data = json.loads(request.body)
    query = data.get('query', '').strip()
    
    if not query:
        return JsonResponse({'error': 'Query is required'}, status=400)
    
    try:
        entry = DictionaryEntry.objects.get(word=query)
        return JsonResponse({'translation': entry.translation, 'source': 'database'})
    except DictionaryEntry.DoesNotExist:
        pass
    
    if is_chinese(query):
        translation = baidu_translate(query, 'zh', 'en')
    else:
        translation = baidu_translate(query, 'en', 'zh')
    
    if translation:
        return JsonResponse({'translation': translation, 'source': 'baidu'})
    else:
        return JsonResponse({'error': 'Translation not found'}, status=404)
