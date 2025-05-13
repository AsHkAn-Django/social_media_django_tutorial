from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + ((_('Additional Info'), {'fields': ('age', 'date_of_birth', 'image')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((_('Additional Info'), {'fields': ('age', 'date_of_birth', 'image')}),)

    list_display = ('username', 'email', 'first_name', 'last_name', 'age', 'date_of_birth', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)
