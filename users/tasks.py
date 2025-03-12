from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_update_course(course_name, emails):
    subject = "Курс обновлен"
    message = (f"Вы подписаны на обновления курса {course_name}.\n"
               "Автор обновил курс, проверьте, что изменилось!")
    send_mail(subject=subject, message=message, recipient_list=emails, from_email=EMAIL_HOST_USER)
