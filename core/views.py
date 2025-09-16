from django.shortcuts import render
from django.views.generic.base import TemplateView

from core.utils import alert_success, alert_error, alert_debug, alert_info, alert_warning

from catalog.services import get_featured

class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_featured())
        context["current_page"] = "HOME"
        return context
    
def home(request):
    alert_success(request,"This is a success message")
    alert_error(request,"This is a error message")
    alert_debug(request,"This is a debug message")
    alert_info(request,"This is a info message")
    alert_warning(request,"This is a warning message")
    return render(request, "core/index.html")
