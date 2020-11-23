from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Group
from .models import *

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': ''}),
        }
        exclude = ['joining_date', 'is_active', 'is_paid', 'updated_by', 'updated_date']


class CompanyUpdateForm(ModelForm):
    class Meta:
        model = Company
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['joining_date', 'is_active', 'is_paid', 'updated_by', 'updated_date']


class CustomUserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm):
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        model = CustomUser
        fields = ('username',)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': ''}),
        }
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'groups', 'is_active')


class MemberForm(ModelForm):
    class Meta:
        model = Member
        widgets = {
            'member_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'nid_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'joining_date': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),            
            'is_active': forms.CheckboxInput(attrs={'class': ''}),
        }
        exclude = ['gym', 'added_by', 'added_date', 'updated_by', 'updated_date']


class TrainerForm(ModelForm):
    class Meta:
        model = Trainer
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'joining_date': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),            
            'is_active': forms.CheckboxInput(attrs={'class': ''}),
        }
        exclude = ['gym', 'added_by', 'added_date', 'updated_by', 'updated_date']


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'payment_month': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),
            'payment_date': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),
            'payment_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }
        exclude = ['gym','added_by', 'added_date', 'updated_by', 'updated_date']

class MemberIncomeForm(ModelForm):
    class Meta:
        model = Income
        widgets = {
            'payment_month': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),
            'payment_date': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),
            'payment_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }
        exclude = ['member', 'gym','added_by', 'added_date', 'updated_by', 'updated_date']


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        widgets = {
            'expense_date': forms.TextInput(attrs={'class': 'form-control jq-datepicker'}),
            'particular': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }
        exclude = ['gym','added_by', 'added_date', 'updated_by', 'updated_date']