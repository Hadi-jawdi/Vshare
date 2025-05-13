from django.urls import path
from . import views_merged

urlpatterns = [
    path('', views_merged.home, name='home'),
    path('profile/', views_merged.profile, name='profile'),
    path('profile/edit/', views_merged.profile_edit, name='profile_edit'),
    path('login/', views_merged.login, name='login'),
    path('logout/', views_merged.logout, name='logout'),
    path('register/', views_merged.register, name='register'),
    path('notifications/', views_merged.notifications, name='notifications'),
    path('messages/', views_merged.messages_view, name='messages'),
    path('like/', views_merged.like_post, name='like_post'),
]
