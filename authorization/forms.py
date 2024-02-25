from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from .models import User


class LoginForm(forms.Form):
    email = forms.CharField(max_length=255, label='',
                            widget=forms.EmailInput(attrs={"class": "form-control form-control-lg border-dark mr-2",
                                                           "placeholder": "Электронная почта", "aria-label": "Email"}))
    password = forms.CharField(max_length=255, label='',
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control form-control-lg border-dark mr-2",
                                          "placeholder": "Пароль", "aria-label": "Пароль"}))


class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=255, label='',
                            widget=forms.EmailInput(attrs={"class": "form-control form-control-lg border-dark mr-2",
                                                           "placeholder": "Электронная почта*",
                                                           "aria-label": "Email"}))
    last_name = forms.CharField(max_length=150, label='',
                                widget=forms.TextInput(attrs={"class": "form-control form-control-lg border-dark mr-2",
                                                              "placeholder": "Фамилия*",
                                                              "aria-label": "Last Name"}))
    first_name = forms.CharField(max_length=150, label='',
                                 widget=forms.TextInput(attrs={"class": "form-control form-control-lg border-dark mr-2",
                                                               "placeholder": "Имя*",
                                                               "aria-label": "First Name"}))
    patronymic = forms.CharField(max_length=150, label='', required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control form-control-lg border-dark mr-2",
                                                               "placeholder": "Отчество",
                                                               "aria-label": "Patronymic"}))
    password1 = forms.CharField(max_length=255, label='',
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control form-control-lg border-dark mr-2",
                                           "placeholder": "Пароль*", "aria-label": "Password1"}))
    password2 = forms.CharField(max_length=255, label='',
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control form-control-lg border-dark mr-2",
                                           "placeholder": "Повторите пароль*", "aria-label": "Password2"}))

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'patronymic', 'password1', 'password2']


class BootstrapErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return mark_safe('<ul class="m-0">%s</ul>' % ''.join(['<li class="text-danger">%s</li>' % e for e in self]))