from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'  # 모델의 모든 필드를 입력받겠다
        labels = {
            'title': '영화 제목',
            'release_year': '개봉 년도',
            'genre': '장르',
            'director': '감독',
            'actors': '주연',
            'rating': '별점',
            'running_time': '러닝타임 (분)',
            'content': '리뷰 내용',
        }