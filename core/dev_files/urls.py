from django.urls import path

from . import email_preview_views

urlpatterns = [
    path("emails/preview/<str:template_name>/", email_preview_views.email_preview, name="email-preview"),
]