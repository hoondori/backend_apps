from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(), name='login'),
  path('user_logout/', auth_views.LogoutView.as_view(), name='user_logout'),
  
  # password change
  path('password-change', auth_views.PasswordChangeView.as_view(), name='password_change'),
  path('password-change-done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
  
  # password reset
  path('password-reset', # prompt user to insert email
       auth_views.PasswordResetView.as_view(), name='password_reset'),
  path('password-reset/done', # notify user that email has been sent.
       auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('password-reset/<uidb64>/<token>/', # url that was sent to email 
       auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('password-reset/complete', # notify user that password reset has ben done.
       auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

  path('', views.dashboard, name='dashboard'),
]
