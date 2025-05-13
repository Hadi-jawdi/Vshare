from django.urls import path
from . import views_post_like

urlpatterns = [
    path('', views_post_like.home, name='home'),
    path('profile/', views_post_like.profile, name='profile'),
    path('profile/edit/', views_post_like.profile_edit, name='profile_edit'),
    path('login/', views_post_like.login, name='login'),
    path('logout/', views_post_like.logout, name='logout'),
    path('register/', views_post_like.register, name='register'),
    path('notifications/', views_post_like.notifications, name='notifications'),
    path('messages/', views_post_like.messages_view, name='messages'),
    path('like/', views_post_like.like_post, name='like_post'),
    path('create_post/', views_post_like.create_post, name='create_post'),
]
