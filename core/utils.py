import os
import uuid
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import environ
from django.template.loader import render_to_string
from django.contrib import messages

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

    logo_url = f"{settings.SITE_URL}{settings.STATIC_URL}core/images/logo.png"

    default_context = {
        "logo_url": logo_url,
        "website_url": settings.SITE_URL,
        "year": datetime.now().year,
    }

    if context:
        default_context.update(context)

    html_content = render_to_string(template_name, default_context)

    email = EmailMultiAlternatives(
            subject = subject,
            body = html_content,
            from_email = settings.EMAIL_DISPLAY,
            to = [to_email],
            reply_to = [MY_EMAIL],
        )
    
    email.attach_alternative(html_content, "text/html")
    email.send()

def alert_success(request, message):
    messages.success(request, message)

def alert_error(request, message):
    messages.error(request, message)

def alert_info(request, message):
    messages.info(request, message)

def alert_warning(request, message):
    messages.warning(request, message)

def alert_debug(request, message):
    messages.debug(request, message)

def new_user_email_admin(user):

    send_email(
        subject = "New User",
        to_email = MY_EMAIL,
        template_name = "core/emails/simple_admin_notification.html",
        context = {
            "subject": "A New User has Registered",
            "message": f"{user.name} ({user.email}) has created an account."
        }
    )

def new_user_confirmation(user):
    send_email(
        subject = "Signup Confirmation",
        to_email = user.email,
        template_name = "core/emails/register_confirmation.html",
        context = {
            "user": user,
        }
    )    