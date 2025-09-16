from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import RegisterUserForm, LoginForm
from .models import CustomUser
from core.utils import new_user_email_admin, new_user_confirmation

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterUserForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("core:home_page")

    def form_valid(self, form):
        response = super().form_valid(form)

        new_user_confirmation(user = self.object)
        new_user_email_admin(user = self.object)

        login(self.request, self.object) 
        return response
    
class LoginView(LoginView):
     template_name = "accounts/login.html"
     authentication_form = LoginForm 
