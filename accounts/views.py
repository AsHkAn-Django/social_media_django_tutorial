from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


class SignUpCreateView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")


User = get_user_model()

class UsersListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "accounts/users.html"
    context_object_name = 'users'


class CLASS_NAME(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/profile.html"

    

