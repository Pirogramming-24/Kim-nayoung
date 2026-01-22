from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import AIHistory
from .services.inference import ai_handler

def index(request):
    return render(request, 'ai_service/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ai_service:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# ai_service/views.py

def translate_view(request):
    result_text = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.POST.get('user_input', '').strip()
        if user_input:
            try:
                target = "en" if any(ord(c) > 128 for c in user_input) else "ko"
                result_text = ai_handler.translate(user_input, target_lang=target)
                
                if request.user.is_authenticated:
                    AIHistory.objects.create(
                        user=request.user, task='translate', input_text=user_input, output_text=result_text
                    )
            except Exception as e:
                result_text = f"에러 발생: {str(e)}"
    
    history = []
    if request.user.is_authenticated:
        history = AIHistory.objects.filter(user=request.user, task='translate').order_by('-created_at')[:5]

    return render(request, 'ai_service/translate.html', {
        'result': result_text, 
        'history': history, 
        'user_input': user_input 
    })


def summarize_view(request):
    if not request.user.is_authenticated:
        return render(request, 'ai_service/alert_login.html', {'next_url': request.path})

    result_text = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.POST.get('user_input', '').strip()
        if user_input:
            try:
                result_text = ai_handler.summarize(user_input)
                
                AIHistory.objects.create(
                    user=request.user, task='summarize', input_text=user_input, output_text=result_text
                )
            except Exception as e:
                result_text = f"에러 발생: {str(e)}"
    
    history = AIHistory.objects.filter(user=request.user, task='summarize').order_by('-created_at')[:5]

    return render(request, 'ai_service/summarize.html', {
        'result': result_text, 
        'history': history, 
        'user_input': user_input 
    })


def generate_view(request):
    if not request.user.is_authenticated:
        return render(request, 'ai_service/alert_login.html', {'next_url': request.path})

    result_text = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.POST.get('user_input', '').strip()
        if user_input:
            try:
                result_text = ai_handler.generate(user_input)
                
                AIHistory.objects.create(
                    user=request.user, task='generate', input_text=user_input, output_text=result_text
                )
            except Exception as e:
                result_text = f"에러 발생: {str(e)}"
    
    history = AIHistory.objects.filter(user=request.user, task='generate').order_by('-created_at')[:5]

    return render(request, 'ai_service/generate.html', {
        'result': result_text, 
        'history': history, 
        'user_input': user_input 
    })