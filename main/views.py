from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DeleteView

from . import forms
from .decorators import superuser_only, writer_only
from .models import Hardware, Facility, FOCL, Muff, Cross, Notification, Port, Adapter


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
    return render(request, 'centers.html', {'title': 'Узлы связи', 'objects': page_objects, 'params': params,
                                            'search_form': search_form, 'sort_form': sort_form})


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
    return render(request, 'muffs.html', {'title': 'Муфты', 'objects': page_objects, 'params': params,
                                          'search_form': search_form, 'sort_form': sort_form})


@writer_only
def muff_create(request):
    context = {'title': 'Добавление муфты'}
    if request.method == 'GET':
        form = forms.MuffForm()
        context['form'] = form
        return render(request, 'create.html', context)

    if request.method == 'POST':
        form = forms.MuffForm(request.POST)
        if form.is_valid():
            muff = form.save(commit=False)
            muff.save()
            return redirect('muffs')
        else:
            context['form'] = form
            return render(request, 'create.html', context)


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
    context = {'title': 'Добавление сооружения связи'}
    if request.method == 'GET':
        form = forms.FacilityForm()
        context['form'] = form
        return render(request, 'create.html', context)

    if request.method == 'POST':
        form = forms.FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.save()
            return redirect('facilities')
        else:
            context['form'] = form
            return render(request, 'create.html', context)


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
    params = {}

    search_form = forms.SearchForm({"search": request.GET.get("search", None)})
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search")
        params['search'] = search_query
        queryset = queryset.filter(cable__marking__icontains=search_query)

    sort_form = forms.FOCLsSortForm({"sorting": request.GET.get("sorting", None)})
    if sort_form.is_valid():
        sort_query = sort_form.cleaned_data.get("sorting")
        if sort_query not in ['-id', 'cable_length']:
            sort_query = '-id'
        params['sorting'] = sort_query
        queryset = queryset.order_by(sort_query)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)

    return render(request, 'focls.html', {'title': 'ВОЛС', 'objects': page_objects, 'params': params,
                                          'search_form': search_form, 'sort_form': sort_form})


@writer_only
def focl_create(request):
    context = {'title': 'Добавление линии связи'}

    if request.method == 'GET':
        form = forms.FOCLForm()
        context['form'] = form
        return render(request, 'focl_create.html', context)

    if request.method == 'POST':
        form = forms.FOCLForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=True)
            current_user = request.user
            if not current_user.is_superuser:
                message = f'Создана новая линия связи между {instance.get_start.name} и {instance.get_end.name}'
                notification = Notification(user=current_user, message=message)
                notification.save()
            return redirect('focls')
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
    return render(request, 'dropdown_list_options.html', {'options': centers})


@login_required
def crosses(request):
    model = Cross
    queryset = model.objects.all().order_by('-id')
    params = {}

    search_form = forms.SearchForm({"search": request.GET.get("search", None)})
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search")
        params['search'] = search_query
        queryset = queryset.filter(facility__name__icontains=search_query)

    sort_form = forms.CrossesSortForm({"sorting": request.GET.get("sorting", None)})
    if sort_form.is_valid():
        sort_query = sort_form.cleaned_data.get("sorting")
        if sort_query not in ['-id', 'adapter_count']:
            sort_query = '-id'
        params['sorting'] = sort_query
        queryset = queryset.order_by(sort_query)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    return render(request, 'crosses.html', {'title': 'Оптические кроссы', 'objects': page_objects, 'params': params,
                                            'search_form': search_form, 'sort_form': sort_form})


@writer_only
def cross_create(request):
    context = {'title': 'Добавление кросса'}

    if request.method == 'GET':
        form = forms.CrossForm()
        context['form'] = form
        return render(request, 'create.html', context)

    if request.method == 'POST':
        form = forms.CrossForm(request.POST)
        if form.is_valid():
            cross = form.save(commit=False)
            cross.save()
            return redirect('crosses')
        else:
            context['form'] = form
    return render(request, 'create.html', context)


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
    ports = object.ports.all()
    return render(request, 'hardware.html', {'title': object.marking, 'object': object, 'ports': ports})


@writer_only
def hardware_create(request):
    context = {'title': 'Добавление оборудования'}

    if request.method == 'GET':
        form = forms.HardwareForm()
        context['form'] = form
        return render(request, 'create.html', context)

    if request.method == 'POST':
        form = forms.HardwareForm(request.POST)
        if form.is_valid():
            hardware = form.save(commit=False)
            hardware.save()
            current_user = request.user
            if not current_user.is_superuser:
                message = f'Добавлено оборудование {hardware.marking} в {hardware.facility.name}'
                notification = Notification(user=current_user, message=message)
                notification.save()
            return redirect('many_hardware')
        else:
            context['form'] = form
            return render(request, 'create.html', context)


class HardwareDelete(DeleteView):
    model = Hardware
    success_url = "/hardware/"


@writer_only
def commutate_port(request, hardware_id, port_id):
    context = {'title': 'Коммутация оборудования', 'hardware_id': hardware_id}

    if request.method == 'GET':
        form = forms.HardwareCommutationForm()
        context['form'] = form
        return render(request, 'hardware_commutation.html', context)

    if request.method == 'POST':
        form = forms.HardwareCommutationForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.start_port = Port.objects.get(pk=port_id)
            connection.save()
            return redirect('hardware', pk=hardware_id)
        else:
            context['form'] = form
            return render(request, 'hardware_commutation.html', context)


@writer_only
def load_port_commutations(request, hardware_id):
    type = request.GET.get('type')
    hardware = Hardware.objects.get(id=hardware_id)
    commutations = []
    facility = hardware.facility

    if type == "adapter":
        if facility.crosses.exists():
            commutations = Adapter.objects.none()
            for object in facility.crosses.all():
                id_list = [adapter.id for adapter in object.adapters.all() if not adapter.is_commutated()]
                commutations |= object.adapters.filter(id__in=id_list, is_linear=False)

    elif type == "port":
        if facility.hardware.exclude(pk=hardware.pk).exists():
            commutations = Port.objects.none()
            for object in facility.hardware.exclude(pk=hardware.pk):
                id_list = [port.id for port in object.ports.all() if not port.is_commutated()]
                commutations |= object.ports.filter(id__in=id_list)
    return render(request, 'dropdown_list_options.html', {'options': commutations})


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


@superuser_only
def load_notifications(request):
    notifications = Notification.objects.all().order_by('is_read', '-id')
    return render(request, 'notifications.html', {'notifications': notifications})


@superuser_only
def read_notification(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.is_read = True
    notification.save()
    return HttpResponse(status=200)


@superuser_only
def delete_notification(request, pk):
    if request.method == 'POST':
        notification = Notification.objects.get(id=pk)
        notification.delete()
        return HttpResponse(status=200)


class NotificationDelete(DeleteView):
    model = Notification

    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        post = self.request.META.get('HTTP_REFERER')
        return post
