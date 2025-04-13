from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('user_logout/', auth_views.LogoutView.as_view(), name='user_logout'),
  path('', views.dashboard, name='dashboard'),
]
