from django.contrib import admin
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ['username', 'email', 'phone', 'date_joined', 'is_staff', 'is_superuser', 'last_login']
    fieldsets = [
        (None, {"fields": ["email", "username", "phone"]}),
        ("Permissions", {"fields": ["is_staff", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "phone", "email", "password1", "password2"],
            },
        ),
    ]
    ordering = ['-date_joined']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_image', 'full_name', 'bio', 'verified', 'is_vendor']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']


admin.site.register(User, UserAdmin)
