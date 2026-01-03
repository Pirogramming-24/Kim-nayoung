from django import forms
from .models import Idea, DevTool

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'image', 'content', 'interest', 'devtool']
        # 입력창을 예쁘게 꾸미기 위한 위젯 설정 (CSS 클래스 같은 것 대신)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디어 명을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '아이디어 설명을 입력하세요', 'rows': 5}),
            'interest': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'devtool': forms.Select(attrs={'class': 'form-control'}),
        }

class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = ['name', 'kind', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '개발툴 이름'}),
            'kind': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '종류 (예: 프레임워크, 라이브러리)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '개발툴 설명', 'rows': 5}),
        }