from django.urls import path
from .views import post_list, like_post, add_comment, post_create, story_create, post_update, post_delete, comment_delete, comment_update, story_view

app_name = 'posts'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('like/', like_post, name='like_post'),
    path('comment/add/', add_comment, name='add_comment'),
    path('create/', post_create, name='post_create'),
    path('story/create/', story_create, name='story_create'),
    path('update/<int:post_id>/', post_update, name='post_update'),
    path('delete/<int:post_id>/', post_delete, name='post_delete'),
    path('comment/delete/', comment_delete, name='comment_delete'),
    path('comment/update/', comment_update, name='comment_update'),
    path('story/<int:story_id>/', story_view, name='story_view'),
]