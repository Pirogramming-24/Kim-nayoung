from django.urls import path
from . import views

app_name = 'ai_service'

urlpatterns = [
    # 메인 페이지 (탭 선택용)
    path('', views.index, name='index'),
    
    # 각 기능별 페이지
    path('translate/', views.translate_view, name='translate'),
    path('summarize/', views.summarize_view, name='summarize'),
    path('generate/', views.generate_view, name='generate'),

    path('signup/', views.signup_view, name='signup'),
]