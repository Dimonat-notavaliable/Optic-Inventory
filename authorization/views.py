from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import get_template
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

            current_context = {
                'name': user.get_full_name,
                'email': user.email,
                'domain': get_current_site(request).domain,
            }
            html_content = get_template('email_template.html').render(current_context)

            mail_subject = f'Новая регистрация: {user.email} - Optic Inventory'
            from_email = 'Optic Inventory <ha.ha.cheetos@gmail.com>'
            to_email = 'ds.shushin@gmail.com'

            msg = EmailMultiAlternatives(mail_subject, '', from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, '''Вы успешно зарегистрировались. Для возможности входа
             в систему вашу учетную запись должен активировать администратор.''')
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
