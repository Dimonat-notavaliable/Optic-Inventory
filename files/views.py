from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime


from .admin import HardwareResource, FacilityResource, MuffResource, CrossResource, FOCLResource
from main.models import Hardware, Facility, Muff, FOCL, Cross


def export_util(dataset, dataset_type, object_description):
    export_time = datetime.datetime.now().strftime("%d-%m-%Y(%H-%M)")
    if dataset_type == 'csv':
        response = HttpResponse(dataset.csv, content_type='application/csv')
        response['Content-Disposition'] = f"attachment; filename=OpticInventory_{object_description}_{export_time}.csv"
    else:
        response = HttpResponse(dataset.xlsx, content_type='application/excel')
        response['Content-Disposition'] = f"attachment; filename=OpticInventory_{object_description}_{export_time}.xlsx"
    return response


@login_required
def export_hardware(request, extension):
    object_type = "Hardware"
    dataset = HardwareResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_one_hardware(request, extension, pk):
    queryset = Hardware.objects.filter(id=pk)
    object_name = f'Hardware_{pk}'
    dataset = HardwareResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


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
