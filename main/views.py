from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .decorators import superuser_only
from .forms import SearchForm, SortForm


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


@superuser_only
def users(request):
    model = get_user_model()
    queryset = model.objects.all().order_by('-id')

    search_form = SearchForm({"search": request.GET.get("search", None)})
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search")
        queryset = queryset.filter(last_name__icontains=search_query)

    sort_form = SortForm({"sorting": request.GET.get("sorting", None)})
    if sort_form.is_valid():
        sort_query = sort_form.cleaned_data.get("sorting")
        if sort_query in ['-id', 'last_name']:
            queryset = queryset.order_by(sort_query)

    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_users = paginator.get_page(page_number)

    return render(request, 'users.html', {'title': 'Пользователи', 'search_form': search_form,
                                          'sort_form': sort_form, 'users': page_users})
