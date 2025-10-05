from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import RegisterUserForm, LoginForm
from .models import CustomUser
from core.helpers.email_utils import new_user_email_admin, new_user_confirmation
from core.helpers.messages import alert_success

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterUserForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("core:home_page")

    def form_valid(self, form):
        response = super().form_valid(form)

        new_user_confirmation(user = self.object)
        new_user_email_admin(user = self.object)

        alert_success(
            self.request,
            f"Welcome, {self.object.name}. Your account has been successfully created!"
        )

        login(self.request, self.object) 
        return response
    
class LoginView(LoginView):
     template_name = "accounts/login.html"
     authentication_form = LoginForm 
