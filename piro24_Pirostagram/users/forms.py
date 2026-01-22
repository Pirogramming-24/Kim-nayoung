from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'profile_image', 'short_description'] 
        # 비밀번호는 UserCreationForm이 알아서 처리해줍니다.