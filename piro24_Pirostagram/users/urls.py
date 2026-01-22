from django.urls import path
from .views import search_users, follow_user, signup, login_view, logout_view

app_name = 'users'

urlpatterns = [
    path('search/', search_users, name='search'),
    path('follow/', follow_user, name='follow'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]