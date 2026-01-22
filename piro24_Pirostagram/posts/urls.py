from django.urls import path
from .views import post_list, like_post

app_name = 'posts'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('like/', like_post, name='like_post'),
]