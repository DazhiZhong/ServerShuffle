from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('reg/', views.register, name='register'),
    path('profile/',views.profile, name='blog_profile'),
    path('login/',auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_conform.html'), name='password_reset_confirm'),
    path('t/',views.newprofile,name='tprofile')
]

# static is only debug 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

