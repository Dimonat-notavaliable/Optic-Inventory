from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'title': 'Главная страница'})


def hardware(request):
    return render(request, 'hardware.html', {'title': 'Оборудование'})
