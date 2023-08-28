from django.urls import path

from users.apps import UsersConfig
from users.views import (
    RegisterView, verify_email, LoginView,
    UserUpdateView, PasswordResetView, PasswordChangeView,
    PasswordChangeDoneView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
)

app_name = UsersConfig.name
urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='users/registration/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/registration/login.html'),
        name='logout'
    ),

    path(
        'register/',
        RegisterView.as_view(
            template_name='users/registration/register.html'
        ),
        name='register'
    ),
    path(
        'verify_email/<uidb64>/<token>/',
        verify_email,
        name='verify_email'
    ),
    path(
        'profile/',
        UserUpdateView.as_view(),
        name='profile'
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name='users/registration/password_reset_form.html'
        ),
        name="password_reset"
    ),
    path(
        "password_reset/sent/",
        PasswordResetDoneView.as_view(
            template_name='users/registration/password_reset_done.html'
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name='users/registration/password_reset_confirm.html'
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name='users/registration/password_reset_complete.html'
        ),
        name="password_reset_complete",
    ),
    path(
        "password_change/", PasswordChangeView.as_view(
            template_name='users/registration/password_change_form.html'
        ),
        name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
