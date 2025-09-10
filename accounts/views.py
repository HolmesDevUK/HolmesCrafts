from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm
from .models import CustomUser

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterUserForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("core:home_page")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object) 
        return response
