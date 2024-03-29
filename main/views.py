from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, CreateView

from .decorators import superuser_only, writer_only
from . import forms
from .models import Hardware, CommunicationCenter, Facility, FOCL, Muff


@login_required
def index(request):
    last_hardware = Hardware.objects.all().order_by('-id')[:5]
    last_focls = FOCL.objects.all().order_by('-id')[:5]
    return render(request, 'index.html', {'title': 'Главная страница',
                                          'last_hardware': last_hardware, 'last_focls': last_focls})


@login_required
def communication_centers(request):
    model = Facility
    queryset = model.objects.all().order_by('-id')

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    return render(request, 'centers.html', {'title': 'Узлы связи', 'objects': page_objects})


@login_required
def facilities(request):
    model = Facility
    queryset = model.objects.all().order_by('-id')
    params = {}

    search_form = forms.SearchForm({"search": request.GET.get("search", None)})
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search")
        params['search'] = search_query
        queryset = queryset.filter(name__icontains=search_query)

    sort_form = forms.CentersSortForm({"sorting": request.GET.get("sorting", None)})
    if sort_form.is_valid():
        sort_query = sort_form.cleaned_data.get("sorting")
        if sort_query not in ['-id', 'name']:
            sort_query = '-id'
        params['sorting'] = sort_query
        queryset = queryset.order_by(sort_query)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    return render(request, 'facilities.html', {'title': 'Сооружения связи', 'objects': page_objects, 'params': params,
                                               'search_form': search_form, 'sort_form': sort_form})


@login_required
def muffs(request):
    model = Muff
    queryset = model.objects.all().order_by('-id')
    params = {}

    search_form = forms.SearchForm({"search": request.GET.get("search", None)})
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search")
        params['search'] = search_query
        queryset = queryset.filter(name__icontains=search_query)

    sort_form = forms.CentersSortForm({"sorting": request.GET.get("sorting", None)})
    if sort_form.is_valid():
        sort_query = sort_form.cleaned_data.get("sorting")
        if sort_query not in ['-id', 'name']:
            sort_query = '-id'
        params['sorting'] = sort_query
        queryset = queryset.order_by(sort_query)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    return render(request, 'muffs.html', {'title': 'Сооружения связи', 'objects': page_objects, 'params': params,
                                          'search_form': search_form, 'sort_form': sort_form})


@writer_only
def muff_create(request):
    if request.method == 'GET':
        form = forms.MuffForm()
        return render(request, 'create.html', {'title': 'Добавление муфты', 'type': "муфты",
                                               'form': form})

    if request.method == 'POST':
        form = forms.MuffForm(request.POST)
        if form.is_valid():
            muff = form.save(commit=False)
            muff.save()
            return redirect('muffs')
        else:
            return render(request, 'create.html', {'title': 'Добавление муфты', 'type': "муфты",
                                                   'form': form})


@login_required
def facilities_map(request):
    model = Facility
    facilities = list(model.objects.values('latitude', 'longitude', 'name'))
    return render(request, 'facilities_map.html', {'title': 'Карта сооружений связи', 'objects': facilities})


@login_required
def muffs_map(request):
    model = Muff
    muffs = list(model.objects.values('latitude', 'longitude', 'name'))
    return render(request, 'facilities_map.html', {'title': 'Карта муфт', 'objects': muffs})


@login_required
def facility(request, pk):
    object = Facility.objects.get(id=pk)
    return render(request, 'facility.html', {'title': object.name, 'object': object})


@writer_only
def facility_create(request):
    if request.method == 'GET':
        form = forms.FacilityForm()
        return render(request, 'create.html', {'title': 'Добавление сооружения связи', 'type': "сооружения связи",
                                               'form': form})

    if request.method == 'POST':
        form = forms.FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.save()
            return redirect('facilities')
        else:
            return render(request, 'create.html', {'title': 'Добавление сооружения связи', 'type': "сооружения связи",
                                                   'form': form})


class FacilityDelete(DeleteView):
    model = Facility
    success_url = "/facilities/"


@login_required
def facility_map(request, pk):
    object = model_to_dict(Facility.objects.get(id=pk))
    return render(request, 'facility_map.html', {'title': f'Карта: {object["name"]}', 'object': object})


@login_required
def focls(request):
    model = FOCL
    queryset = model.objects.all().order_by('-id')
    return render(request, 'focls.html', {'title': 'ВОЛС', 'objects': queryset})


@login_required
def many_hardware(request):
    model = Hardware
    queryset = model.objects.all().order_by('-id')
    params = {}

    search_form = forms.SearchForm({"search": request.GET.get("search", None)})
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search")
        params['search'] = search_query
        queryset = queryset.filter(marking__icontains=search_query)

    sort_form = forms.HardwareSortForm({"sorting": request.GET.get("sorting", None)})
    if sort_form.is_valid():
        sort_query = sort_form.cleaned_data.get("sorting")
        if sort_query not in ['-id', 'marking']:
            sort_query = '-id'
        params['sorting'] = sort_query
        queryset = queryset.order_by(sort_query)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    return render(request, 'many_hardware.html', {'title': 'Оборудование', 'objects': page_objects, 'params': params,
                                                  'search_form': search_form, 'sort_form': sort_form})


@login_required
def hardware(request, pk):
    object = Hardware.objects.get(id=pk)
    return render(request, 'hardware.html', {'title': object.marking, 'object': object})


@writer_only
def hardware_create(request):
    if request.method == 'GET':
        form = forms.HardwareForm()
        return render(request, 'create.html', {'title': 'Добавление оборудования', 'type': "оборудования",
                                               'form': form})

    if request.method == 'POST':
        form = forms.HardwareForm(request.POST)
        if form.is_valid():
            hardware = form.save(commit=False)
            hardware.save()
            return redirect('many_hardware')
        else:
            return render(request, 'create.html', {'title': 'Добавление оборудования', 'type': "оборудования",
                                                   'form': form})


class HardwareDelete(DeleteView):
    model = Hardware
    success_url = "/hardware/"


@superuser_only
def users(request):
    model = get_user_model()
    queryset = model.objects.all().order_by('-id')
    params = {}

    search_form = forms.SearchForm({"search": request.GET.get("search", None)})
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search")
        params['search'] = search_query
        queryset = queryset.filter(last_name__icontains=search_query)

    sort_form = forms.UsersSortForm({"sorting": request.GET.get("sorting", None)})
    if sort_form.is_valid():
        sort_query = sort_form.cleaned_data.get("sorting")
        if sort_query not in ['-id', 'last_name']:
            sort_query = '-id'
        params['sorting'] = sort_query
        queryset = queryset.order_by(sort_query)

    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)

    return render(request, 'users.html', {'title': 'Пользователи', 'objects': page_objects, 'params': params,
                                          'search_form': search_form, 'sort_form': sort_form})


@writer_only
def focl_create(request):
    context = {'title': 'Добавление линии связи', 'type': "линия связи"}

    if request.method == 'GET':
        form = forms.FOCLForm()
        context['form'] = form
        return render(request, 'focl_create.html', context)

    if request.method == 'POST':
        form = forms.FOCLForm(request.POST)
        if form.is_valid():
            _ = form.save(commit=False)
            return redirect('home')
        else:
            context['form'] = form
    return render(request, 'focl_create.html', context)


@writer_only
def load_centers(request):
    type = request.GET.get('type')
    centers = []
    if type == "muff":
        centers = Muff.objects.all().order_by('name')
    elif type == "facility":
        centers = Facility.objects.all().order_by('name')
    return render(request, 'center_dropdown_list_options.html', {'centers': centers})