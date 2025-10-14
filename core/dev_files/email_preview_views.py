from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from datetime import date
from premailer import transform
from django.conf import settings

def email_preview(request, template_name):
    
    if not settings.DEBUG:
        return HttpResponseForbidden("Email preview is not available in production.")

    context = {
        "customer": {"name": "Aaron Holmes", "email": "aaron@example.com"},
        "order": {
            "items": [
                {"product_name": "Test Product A", "quantity": 2},
                {"product_name": "Test Product B", "quantity": 1},
            ]
        },
        "shipping_address": {
            "line1": "123 Example Street",
            "city": "London",
            "postcode": "E1 1AA",
        },
        "year": date.today().year,
        "logo_url": "https://holmescrafts.com/static/images/logo.png",
        "website_url": "https://holmescrafts.com",
    }

  
    html_content = render_to_string(f"core/emails/{template_name}.html", context)

    
    inlined_html = transform(html_content)

    
    return HttpResponse(inlined_html)
