# urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Other URL patterns...
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="poll/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="poll/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="poll/reset_password_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="poll/reset_password_complete.html"), name="password_reset_complete"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

]
