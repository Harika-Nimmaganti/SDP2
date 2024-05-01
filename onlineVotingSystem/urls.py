from django.contrib import admin
from django.urls import path
from poll import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.homeView, name='home'),
    path('register/', views.registrationView, name='registration'),
    path('login/', views.loginView, name='login'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
    path('position/', views.positionView, name='position'),
    path('candidate/<int:pos>/', views.candidateView, name='candidate'),
    path('candidate/detail/<int:id>/', views.candidateDetailView, name='detail'),
    path('result/', views.resultView, name='result'),
    path('changepass/', views.changePasswordView, name='changepass'),
    path('editprofile/', views.editProfileView, name='editprofile'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="poll/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="poll/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="poll/reset_password_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="poll/reset_password_complete.html"), name="password_reset_complete"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
