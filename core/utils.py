from django.conf import settings
import os
import uuid
from datetime import datetime

def absolute_url(url:str, request=None) -> str:
    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    if request:
        return request.build_absolute_uri(url)
    return f"{settings.SITE_URL.rstrip('/')}{url}"

def upload_to(instance, filename):
    
    app_name = instance._meta.app_label
    folder_name = instance.__class__.__name__.lower()
    
    
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    
    date_path = datetime.now().strftime("%Y/%m/%d")
    
    return os.path.join(app_name, folder_name, date_path, filename)