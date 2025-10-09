from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

my_email = settings.MY_EMAIL
from_email = settings.EMAIL_DISPLAY

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
            from_email = from_email,
            to = [to_email],
            reply_to = [my_email],
        )
    
    email.attach_alternative(html_content, "text/html")
    email.send()

def new_user_email_admin(user):

    send_email(
        subject = "New User",
        to_email = my_email,
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

def order_confirmation_admin(data):
    send_email(
        subject = "New Order",
        to_email = my_email,
        template_name = "core/emails/order_confirmation_admin.html",
        context = data,
    )   
