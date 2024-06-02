from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

from .forms import ImportForm
from .admin import HardwareExportResource, FacilityResource, MuffResource, CrossResource, FOCLResource, \
    HardwareImportResource
from import_export import resources
from main.models import Hardware, Facility, Muff, FOCL, Cross
from tablib import Dataset


def export_util(dataset, dataset_type, object_description):
    export_time = datetime.datetime.now().strftime("%d-%m-%Y(%H-%M)")
    if dataset_type == 'csv':
        response = HttpResponse(dataset.csv, content_type='application/csv')
        response['Content-Disposition'] = f"attachment; filename=OpticInventory_{object_description}_{export_time}.csv"
    else:
        response = HttpResponse(dataset.xlsx, content_type='application/excel')
        response['Content-Disposition'] = f"attachment; filename=OpticInventory_{object_description}_{export_time}.xlsx"
    return response


def import_util(request, resource, headers, import_url, success_url):
    file = request.FILES['file']
    dataset_type = file.name.split('.')[-1]

    dataset = Dataset(headers=headers)
    dataset.load(file.read(), format=dataset_type)

    result = resource.import_data(dataset, dry_run=True, raise_errors=True)  # Dry run to check for errors

    if not result.has_errors():
        resource.import_data(dataset, dry_run=False)  # Actually import now
        messages.success(request, "Импорт завершен.")
        return success_url
    else:
        messages.error(request, "Импорт не удался. Пожалуйста, проверьте формат файла и целостность данных.")
        return import_url


@login_required
def export_hardware(request, extension):
    object_type = "Hardware"
    dataset = HardwareExportResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_one_hardware(request, extension, pk):
    queryset = Hardware.objects.filter(id=pk)
    object_name = f'Hardware_{pk}'
    dataset = HardwareExportResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@login_required
def import_hardware(request):
    headers_file = 'xlsx/OpticInventory_Заголовки_Оборудование.xlsx'
    title = "Импорт оборудования"
    redirect_url = 'import_hardware'
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = HardwareImportResource()
            headers = ['id', 'facility', 'floor', 'marking', 'type', 'IP', 'MAC', 'port_count']
            redirect_url = import_util(request, resource, headers,
                                       import_url='import_hardware', success_url='many_hardware')
        return redirect(redirect_url)
    else:
        form = ImportForm()
    return render(request, 'import.html', {'title': title, 'form': form,
                                           'headers_file': headers_file})


@login_required
def export_facilities(request, extension):
    object_type = "Facilities"
    dataset = FacilityResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_facility(request, extension, pk):
    queryset = Facility.objects.filter(id=pk)
    object_name = f'Facility_{pk}'
    dataset = FacilityResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@login_required
def export_muffs(request, extension):
    object_type = "Muffs"
    dataset = MuffResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_muff(request, extension, pk):
    queryset = Muff.objects.filter(id=pk)
    object_name = f'Muff_{pk}'
    dataset = MuffResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@login_required
def export_focls(request, extension):
    object_type = "FOCLs"
    dataset = FOCLResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_focl(request, extension, pk):
    queryset = FOCL.objects.filter(id=pk)
    object_name = f'FOCL_{pk}'
    dataset = FOCLResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@login_required
def export_crosses(request, extension):
    object_type = "Crosses"
    dataset = CrossResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_cross(request, extension, pk):
    queryset = Cross.objects.filter(id=pk)
    object_name = f'Cross_{pk}'
    dataset = CrossResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response
