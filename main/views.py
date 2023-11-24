from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html', {'title': 'Главная страница'})


@login_required
def hardware(request):
    return render(request, 'hardware.html', {'title': 'Оборудование'})
