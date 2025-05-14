from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from .models import Follow




class SignUpCreateView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")


User = get_user_model()


class UsersListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "accounts/users.html"
    context_object_name = 'users'



class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "accounts/profile_detail.html"
    context_object_name = 'user'



class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = "accounts/profile_update.html"
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None):
        # This restricts editing to the logged-in user only
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'password' in form.fields:
            form.fields.pop('password')  # Remove password from the form dynamically
        return form
    
    

def follow_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    follower = request.user
    
    follower_exist = Follow.objects.filter(user=user, follower=follower)
    if follower_exist:
        follower_exist.delete()
        return redirect('accounts:users')
    Follow.objects.create(user=user, follower=follower)
    return redirect('accounts:users')
        