from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_page, name='index'),
    path('api/', views.chat_api, name='api'),
]