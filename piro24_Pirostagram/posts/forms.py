from django import forms
from .models import Post, Story

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content'] # 사용자는 이미지는 내용만 입력하면 됨 (작성자는 자동)
        
        # 폼 디자인을 위한 위젯 설정
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '문구 입력...', 'rows': 3}),
        }

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image'] # 스토리는 사진만 올리면 됨