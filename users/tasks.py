from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER

from .models import CustomUser


@shared_task
def send_mail_update_course(course_name, emails):
    """
    Задача для исполнения в параллельном потоке. Принимает
    название курса и список email-адресов для отправки уведомления об обновлении курса.
    """

    subject = "Курс обновлен"
    message = (f"Вы подписаны на обновления курса {course_name}.\n"
               "Автор обновил курс, проверьте, что изменилось!")
    send_mail(subject=subject, message=message, recipient_list=emails, from_email=EMAIL_HOST_USER)


@shared_task
def block_users_last_login_more_month():
    """
    Периодическая задача для исполнения в параллельном потоке. Блокирует пользователей,
    которые не автризовывались более 30 дней. Устанавливает поле is_active = False.
    """

    date_start_month = timezone.now() - timedelta(days=30)
    old_users = CustomUser.objects.filter(last_login__lt=date_start_month)
    for user in old_users:
        user.is_active = False
        user.save()
