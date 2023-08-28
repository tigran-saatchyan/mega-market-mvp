from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import (
    PasswordChangeDoneView as BasePasswordChangeDoneView
)
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView
)
from django.contrib.auth.views import (
    PasswordResetCompleteView as BasePasswordResetCompleteView
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.contrib.auth.views import (
    PasswordResetDoneView as BasePasswordResetDoneView
)
from django.contrib.auth.views import (
    PasswordResetView as BasePasswordResetView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView

from users.forms import RegisterForm, LoginForm, UserChangeForm, \
    PasswordResetForm, PasswordChangeForm, SetPasswordForm
from users.models import User


# Чаще всего применяются:
# LoginView — контроллер авторизации.
# LogoutView — контроллер выхода.


# Реже применяются:

# PasswordResetView — контроллер для запуска процесса сброса пароля.

# PasswordChangeView — контроллер для смены пароля, то есть ввода данных.

# PasswordChangeDoneView — контроллер для отображения страницы успешного
#   заполнения данных.

# PasswordResetConfirmView — контроллер для подтверждения сброса пароля.

# PasswordResetCompleteView — контроллер для отображения страницы
#   успешного сброса пароля.

# PasswordResetDoneView — контроллер для отображения страницы завершения
#   процесса сброса пароля.
#
# LoginView
# LogoutView
#
# PasswordResetView
# PasswordChangeView
# PasswordChangeDoneView
# PasswordResetConfirmView
# PasswordResetCompleteView
# PasswordResetDoneView

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.is_active)
        )


generate_token = TokenGenerator()


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')

    def send_verification_email(self, user):
        token = generate_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = 'Подтверждение электронной почты'
        message = render_to_string(
            'users/registration/verification_email.html',
            {
                'user': user,
                'uid': uid,
                'domain': current_site.domain,
                'token': token
            }
        )

        send_mail(
            subject=mail_subject,
            message=message,
            from_email=None,
            recipient_list=[user.email],
            html_message=message
        )

    def form_valid(self, form):
        self.object = form.save()
        self.send_verification_email(self.object)
        return super().form_valid(form)


def verify_email(request, uidb64, token):
    data = {}
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(
            user, token
    ):

        user.is_verified = True
        user.save()

        return render(
            request,
            'users/registration/email_verified.html',
            context=data
        )

    return render(
        request,
        'users/registration/email_verified.html',
        context=data
    )


class LoginView(BaseLoginView):
    form_class = LoginForm


class LogoutView(BaseLogoutView):
    pass


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserChangeForm

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(BasePasswordResetView):
    model = User
    form_class = PasswordResetForm
    email_template_name = 'users/registration/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetDoneView(BasePasswordResetDoneView):
    pass


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    pass


class PasswordChangeView(BasePasswordChangeView):
    model = User
    form_class = PasswordChangeForm


class PasswordChangeDoneView(BasePasswordChangeDoneView):
    model = User
