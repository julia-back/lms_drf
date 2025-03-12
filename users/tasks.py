from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_mail_update_course(course_name, emails):
    subject = "Курс обновлен"
    message = (f"Вы подписаны на обновления курса {course_name}.\n"
               "Автор обновил курс, проверьте, что изменилось!")
    send_mail(subject=subject, message=message, recipient_list=emails, from_email=EMAIL_HOST_USER)


@shared_task
def block_users_last_login_more_month():
    date_start_month = timezone.now() - timedelta(days=30)
    old_users = CustomUser.objects.filter(last_login__lt=date_start_month)
    for user in old_users:
        user.is_active = False
        user.save()
