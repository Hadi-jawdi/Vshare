from django.urls import path
from . import views_fixed

urlpatterns = [
    path('', views_fixed.home, name='home'),
    path('profile/', views_fixed.profile, name='profile'),
    path('profile/edit/', views_fixed.profile_edit, name='profile_edit'),
    path('login/', views_fixed.login, name='login'),
    path('logout/', views_fixed.logout, name='logout'),
    path('register/', views_fixed.register, name='register'),
    path('notifications/', views_fixed.notifications, name='notifications'),
    path('messages/', views_fixed.messages_view, name='messages'),
    path('like/', views_fixed.like_post, name='like_post'),
]
