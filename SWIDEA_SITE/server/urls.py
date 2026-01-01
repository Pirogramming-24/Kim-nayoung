from django.urls import path
from . import views

app_name = 'server'

urlpatterns = [
    path('', views.main, name='main'),

    path('create/', views.idea_create, name='idea_create'),
    path('<int:pk>/', views.idea_detail, name='idea_detail'),
    path('<int:pk>/update/', views.idea_update, name='idea_update'),
    path('<int:pk>/delete/', views.idea_delete, name='idea_delete'),

    path('devtool/', views.devtool_list, name='devtool_list'),
    path('devtool/create/', views.devtool_create, name='devtool_create'),
    path('devtool/<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('devtool/<int:pk>/update/', views.devtool_update, name='devtool_update'),
    path('devtool/<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),

    path('star/<int:pk>/', views.idea_star, name='idea_star'),
    path('interest/<int:pk>/', views.idea_interest, name='idea_interest'),
]