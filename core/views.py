from django.shortcuts import render
from django.views.generic.base import TemplateView

from catalog.services import get_featured

class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_featured())
        context["current_page"] = "HOME"
        return context
