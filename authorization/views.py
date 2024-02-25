from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, BootstrapErrorList


def sign_up(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

        form = RegisterForm()
        return render(request, 'register.html', {'title': 'Регистрация', 'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=BootstrapErrorList)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect('home')
        else:
            return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        return render(request, 'login.html', {'title': 'Вход', 'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST, error_class=BootstrapErrorList)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Здравствуйте, {user.first_name}!')
                return redirect('home')
        # form is not valid or user is not authenticated
        messages.error(request, 'Неверный адрес почты или пароль')
        return render(request, 'login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('login')
