from django.urls import path
from .views import post_list, like_post, add_comment, post_create, story_create

app_name = 'posts'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('like/', like_post, name='like_post'),
    path('comment/add/', add_comment, name='add_comment'),
    path('create/', post_create, name='post_create'),
    path('story/create/', story_create, name='story_create'),
]