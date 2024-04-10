from celery import shared_task
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST


@shared_task
def send_email_task(email, code):
    send_mail(
        'Change Password OTP Code',
        f'Dear user,\nyour otp to login is {code}',
        from_email=EMAIL_HOST,
        recipient_list=[email]
    )


@shared_task
def sending_weekly_schedule(student, unit_form):
    x = ""
    for item in unit_form.course.all():
        x += f"class number: {item.class_id} - day: {item.day} - time: {item.time}\n"
    send_mail(
        subject='weekly schedule',
        message=x,
        from_email=EMAIL_HOST,
        recipient_list=[student.email]
    )
