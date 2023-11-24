from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login


def index(request):
    return render(request, 'users.html', {'title': 'Пользователи'})
