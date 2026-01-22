import json
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()

# 1. 회원가입
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user) # 가입 후 바로 로그인 처리
            return redirect('posts:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# 2. 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('posts:post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# 3. 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')

def search_users(request):
    query = request.GET.get('q') # 검색어 가져오기 (?q=검색어)
    results = []
    
    if query:
        # 아이디(username)에 검색어가 포함된 유저 찾기 (icontains: 대소문자 무시)
        results = User.objects.filter(username__icontains=query)
        
    return render(request, 'users/search.html', {'results': results, 'query': query})

@login_required
@csrf_exempt
def follow_user(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        target_id = req.get('user_id')
        target_user = get_object_or_404(User, id=target_id)
        
        # 자기 자신 팔로우 방지
        if target_user == request.user:
            return JsonResponse({'message': 'error'}, status=400)
            
        # 팔로우 로직 (user.following: 내가 팔로우 하는 사람들)
        if target_user in request.user.following.all():
            request.user.following.remove(target_user)
            is_followed = False
        else:
            request.user.following.add(target_user)
            is_followed = True
            
        return JsonResponse({'is_followed': is_followed})