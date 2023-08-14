from django.core import mail


def send_mail(subject, message, to_email, from_email=None):
    mail.send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[to_email],
        html_message=message
    )
