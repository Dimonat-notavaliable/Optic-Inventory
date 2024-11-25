from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, UpdateView

from . import forms
from .decorators import superuser_only, writer_only, login_required
from .models import Hardware, Facility, FOCL, Muff, Cross, Notification, Port, Adapter
from .utils import get_modules_info

import json
import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    last_hardware = Hardware.objects.all().order_by('-id')[:5]
    last_focls = FOCL.objects.all().order_by('-id')[:5]
    return render(request, 'index.html', {'title': 'Главная страница',
                                          'last_hardware': last_hardware, 'last_focls': last_focls})


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
    if page_number:
        counter_addition = (int(page_number) - 1) * 10
    else:
        counter_addition = 0
    page_objects = paginator.get_page(page_number)
    return render(request, 'many_objects/facilities.html',
                  {'title': 'Сооружения связи', 'objects': page_objects, 'params': params,
                   'search_form': search_form, 'sort_form': sort_form, 'addition': counter_addition})


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
    if page_number:
        counter_addition = (int(page_number) - 1) * 10
    else:
        counter_addition = 0
    page_objects = paginator.get_page(page_number)
    return render(request, 'many_objects/muffs.html', {'title': 'Муфты', 'objects': page_objects, 'params': params,
                                                       'search_form': search_form, 'sort_form': sort_form,
                                                       'addition': counter_addition})


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


class FacilityDelete(DeleteView):
    model = Facility
    success_url = "/facilities/"


class FacilityUpdate(UpdateView):
    model = Facility
    success_url = '/facilities/'
    form_class = forms.FacilityForm
    template_name = "edit.html"


class MuffDelete(DeleteView):
    model = Muff
    success_url = "/muffs/"


class MuffUpdate(UpdateView):
    model = Muff
    success_url = '/muffs/'
    form_class = forms.MuffForm
    template_name = "edit.html"


@login_required
def facilities_map(request):
    model = Facility
    facilities = list(model.objects.values('latitude', 'longitude', 'name'))
    return render(request, 'maps_html/many_map.html', {'title': 'Карта сооружений связи', 'objects': facilities})


@login_required
def muffs_map(request):
    model = Muff
    muffs = list(model.objects.values('latitude', 'longitude', 'name'))
    return render(request, 'maps_html/many_map.html', {'title': 'Карта муфт', 'objects': muffs})


@login_required
def facility(request, pk):
    model = Facility
    object = model.objects.get(id=pk)
    hardware = object.hardware.all()
    connections = object.connection.all()
    return render(request, 'single_object/facility.html', {'title': object.name, 'object': object,
                                                           'many_hardware': hardware, 'connections': connections})


@login_required
def muff(request, pk):
    model = Muff
    object = model.objects.get(id=pk)
    connections = object.connection.all()
    return render(request, 'single_object/muff.html', {'title': object.name, 'object': object,
                                                       'connections': connections})


@login_required
def facility_map(request, pk):
    object = model_to_dict(Facility.objects.get(id=pk))
    return render(request, 'maps_html/single_map.html', {'title': f'Карта: {object["name"]}', 'object': object})


@login_required
def muff_map(request, pk):
    object = model_to_dict(Muff.objects.get(id=pk))
    return render(request, 'maps_html/single_map.html', {'title': f'Карта: {object["name"]}', 'object': object})


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
    if page_number:
        counter_addition = (int(page_number) - 1) * 10
    else:
        counter_addition = 0
    page_objects = paginator.get_page(page_number)

    return render(request, 'many_objects/focls.html', {'title': 'ВОЛС', 'objects': page_objects, 'params': params,
                                                       'search_form': search_form, 'sort_form': sort_form,
                                                       'addition': counter_addition})


@login_required
def focl(request, pk):
    model = FOCL
    object = model.objects.get(id=pk)
    start = object.get_start()
    end = object.get_end()
    start_modules = object.cable.modules.all().order_by('number')
    end_modules = object.cable.modules.all().order_by('number')

    start_modules_info = get_modules_info(start_modules, start)
    end_modules_info = get_modules_info(end_modules, end)

    all_connections = zip([start.name, end.name],
                          [start_modules_info, end_modules_info])

    return render(request, 'single_object/focl.html', {'title': object, 'object': object,
                                                       'start': start, 'end': end,
                                                       'connections': all_connections})


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


class FOCLDelete(DeleteView):
    model = FOCL
    success_url = "/focls/"


class FOCLUpdate(UpdateView):
    model = FOCL
    success_url = '/focls/'
    form_class = forms.FOCLForm
    template_name = "edit.html"


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
    if page_number:
        counter_addition = (int(page_number) - 1) * 10
    else:
        counter_addition = 0
    page_objects = paginator.get_page(page_number)
    return render(request, 'many_objects/crosses.html',
                  {'title': 'Оптические кроссы', 'objects': page_objects, 'params': params,
                   'search_form': search_form, 'sort_form': sort_form, 'addition': counter_addition})


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


class CrossDelete(DeleteView):
    model = Cross
    success_url = "/crosses/"


class CrossUpdate(UpdateView):
    model = Cross
    success_url = '/crosses/'
    form_class = forms.CrossForm
    template_name = "edit.html"


@login_required
def cross(request, pk):
    model = Cross
    object = model.objects.get(id=pk)
    linear_adapters = object.adapters.filter(is_linear=True).order_by("number")
    station_adapters = object.adapters.filter(is_linear=False).order_by("number")
    adapters = zip(linear_adapters, station_adapters)
    return render(request, 'single_object/cross.html', {'title': object, 'object': object, 'adapters': adapters})


@writer_only
def commutate_linear_adapter(request, cross_id, adapter_id):
    context = {'title': 'Коммутация кросса', 'cross_id': cross_id}

    if request.method == 'GET':
        form = forms.LinearAdapterCommutationForm(cross_id)
        context['form'] = form
        return render(request, 'create.html', context)

    if request.method == 'POST':
        form = forms.LinearAdapterCommutationForm(cross_id, request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            adapter = Adapter.objects.get(pk=adapter_id)
            connection.end_adapter = adapter
            connection.facility = adapter.cross.facility
            connection.save()
            return redirect('cross', pk=cross_id)
        else:
            context['form'] = form
            return render(request, 'create.html', context)


@writer_only
def commutate_station_adapter(request, cross_id, adapter_id):
    context = {'title': 'Коммутация кросса', 'cross_id': cross_id}

    if request.method == 'GET':
        form = forms.StationAdapterCommutationForm(cross_id)
        context['form'] = form
        return render(request, 'create.html', context)

    if request.method == 'POST':
        form = forms.StationAdapterCommutationForm(cross_id, request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            adapter = Adapter.objects.get(pk=adapter_id)
            connection.start_adapter = adapter
            connection.facility = adapter.cross.facility
            connection.save()
            return redirect('cross', pk=cross_id)
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
    if page_number:
        counter_addition = (int(page_number) - 1) * 10
    else:
        counter_addition = 0
    page_objects = paginator.get_page(page_number)
    return render(request, 'many_objects/many_hardware.html',
                  {'title': 'Оборудование', 'objects': page_objects, 'params': params,
                   'search_form': search_form, 'sort_form': sort_form, 'addition': counter_addition})


@login_required
def hardware(request, pk):
    object = Hardware.objects.get(id=pk)
    ports = object.ports.all()
    return render(request, 'single_object/hardware.html', {'title': object.marking, 'object': object, 'ports': ports})


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


class HardwareUpdate(UpdateView):
    model = Hardware
    success_url = '/hardware/'
    form_class = forms.HardwareForm
    template_name = "edit.html"


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
            connection.end_port = Port.objects.get(pk=port_id)
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
    queryset = model.objects.all().order_by('-id').exclude(id=request.user.id)
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

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    if page_number:
        counter_addition = (int(page_number) - 1) * 10
    else:
        counter_addition = 0
    page_objects = paginator.get_page(page_number)

    return render(request, 'many_objects/users.html',
                  {'title': 'Пользователи', 'objects': page_objects, 'params': params,
                   'search_form': search_form, 'sort_form': sort_form, 'addition': counter_addition})


@superuser_only
@csrf_exempt
@require_POST
def update_user(request):
    model = get_user_model()

    changes = json.loads(request.POST.get('changes'))
    for change in changes:
        user_id = change['user_id']
        field = change['field']
        value = change['value']

        user = model.objects.get(id=user_id)
        setattr(user, field, value)
        user.save()

    return JsonResponse({'success': True})


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
