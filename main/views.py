from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html', {'title': 'Главная страница'})


@login_required
def facilities(request):
    return render(request, 'facilities.html', {'title': 'Сооружения связи'})


@login_required
def focls(request):
    return render(request, 'focls.html', {'title': 'Кабельная инфраструктура'})


@login_required
def hardware(request):
    return render(request, 'hardware.html', {'title': 'Оборудование'})


@login_required
def users(request):
    if request.user.is_superuser:
        model = get_user_model()
        users = model.objects.all()
        return render(request, 'users.html', {'title': 'Пользователи', 'users': users})
    else:
        return redirect('home')
