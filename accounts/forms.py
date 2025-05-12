from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email        
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'image', 'age', 'date_of_birth', 'first_name', 'last_name')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_email = CustomUser.objects.exclude(id=self.instance.id).filter(email=email)
        if user_email.exists():
            raise forms.ValidationError("Email already exists.")
        return email