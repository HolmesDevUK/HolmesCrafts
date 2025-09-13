import os
import uuid
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import environ
from django.template.loader import render_to_string

env = environ.Env()

MY_EMAIL = env("MY_EMAIL")

def upload_to(instance, filename):
    
    app_name = instance._meta.app_label
    folder_name = instance.__class__.__name__.lower()
    
    
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    
    date_path = datetime.now().strftime("%Y/%m/%d")
    
    return os.path.join(app_name, folder_name, date_path, filename)

def send_email(subject: str, to_email: str, template_name: str, context: dict = None):

    context = context or {}

    html_content = render_to_string(template_name, context)

    email = EmailMultiAlternatives(
            subject = subject,
            body = html_content,
            from_email = settings.EMAIL_DISPLAY,
            to = [to_email],
            reply_to = MY_EMAIL
        )
    
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_me_email(subject, message):
    send_email(subject, message, MY_EMAIL)