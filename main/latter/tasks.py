from celery import shared_task
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .models import Client, Mailing, MailingLog

@shared_task
def send_message(message_id):
    message = Mailing.objects.get(id=message_id)
    clients = Client.objects.filter(id__in=message.recipients)
    for client in clients:
        # отправка сообщения клиенту
        status = send_to_external_service(client.email, message.text)
        # создание объекта лога
        log = MailingLog.objects.create(
            message=message,
            client=client,
            status=status
        )

def send_email(request):
    mailing = Mailing.objects.get(title="Важно")  # Get the specific Mailing object with the desired title
    title = mailing.title
    content = mailing.content

    # Get the list of clients
    clients = Client.objects.all()

    # Create a list of email addresses from the clients list
    recipient_list = [client.email for client in clients]

    # Send the email to all addresses in recipient_list
    send_mail(title, content, settings.EMAIL_HOST_USER, recipient_list)
    return render(request, "latter/email_complete.html")

@shared_task
def schedule_message(message_id):
    message = Mailing.objects.get(id=message_id)
    start_time = datetime.combine(message.start_date, message.start_time)
    end_time = datetime.combine(message.end_date, message.end_time)
    if start_time <= datetime.now() <= end_time:
        send_message.delay(message.id)
