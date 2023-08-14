from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers


def say_hello(request):
    try:
        notify_customers.delay('hello')
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Tarak'})
