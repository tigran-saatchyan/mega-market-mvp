from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание супер-пользователя admin@evoq.com'

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='admin@evoq.com',
            first_name='Admin',
            last_name='EvoQ',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('QWE123rty')
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Супер-Пользователь {user.email} создан'
            )
        )
