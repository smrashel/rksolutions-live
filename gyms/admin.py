from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('name', 'contact_number', 'email_address', 'address', 'joining_date', 'is_active', 'is_paid',)
    list_filter = ('is_active', 'is_paid',)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'company_name', 'is_staff', 'is_active',)
    list_filter = ('company_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'username', 'company_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username', 'company_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Member)
admin.site.register(Income)
admin.site.register(Expense)
