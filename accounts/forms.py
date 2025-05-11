from django.forms import Form
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import AbstractUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AbstractUser
        fields = UserCreationForm.Meta.fields + ('age', 'date_of_birth', 'image',)