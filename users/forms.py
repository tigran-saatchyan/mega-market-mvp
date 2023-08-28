from django.contrib.auth.forms import (
    PasswordChangeForm as BasePasswordChangeForm
)
from django.contrib.auth.forms import (
    PasswordResetForm as BasePasswordResetForm
)
from django.contrib.auth.forms import (
    SetPasswordForm as BaseSetPasswordForm
)
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import HiddenInput

from catalog.forms import StyleFormMixin
from users.models import User


# UserCreationForm — создание или регистрация пользователя.
# UserChangeForm — редактирование данных пользователя.
# AuthenticationForm — авторизация пользователя.
# PasswordChangeForm — изменение пароля пользователем.
# PasswordResetForm — сброс пароля пользователем.
# SetPasswordForm — установка пароля пользователем.


class RegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class LoginForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('__all__',)


class UserChangeForm(StyleFormMixin, BaseUserChangeForm):
    class Meta:
        model = User
        fields = (
            'avatar',
            'email',
            'password',
            'first_name',
            'last_name',
            'telephone',
            'country',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = HiddenInput()


class PasswordResetForm(StyleFormMixin, BasePasswordResetForm):
    email_template_name = 'users/registration/password_reset_email.html'


class SetPasswordForm(StyleFormMixin, BaseSetPasswordForm):
    class Meta:
        model = User
        fields = ('__all__',)


class PasswordChangeForm(BasePasswordChangeForm):
    pass
