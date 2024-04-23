from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime


from .admin import HardwareResource, FacilityResource, MuffResource, CrossResource, FOCLResource


def export_util(dataset, dataset_type, object_type):
    export_time = datetime.datetime.now().strftime("%d-%m-%Y(%H:%M)")
    if dataset_type == 'csv':
        response = HttpResponse(dataset.csv, content_type='application/csv')
        response['Content-Disposition'] = f"attachment; filename=OpticInventory_{object_type}_{export_time}.csv"
    else:
        response = HttpResponse(dataset.xlsx, content_type='application/excel')
        response['Content-Disposition'] = f"attachment; filename=OpticInventory_{object_type}_{export_time}.xlsx"
    return response


@login_required
def export_hardware(request, extension):
    object_type = "Hardware"
    dataset = HardwareResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_facilities(request, extension):
    object_type = "Facilities"
    dataset = FacilityResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_muffs(request, extension):
    object_type = "Muffs"
    dataset = MuffResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_focls(request, extension):
    object_type = "FOCLs"
    dataset = FOCLResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_crosses(request, extension):
    object_type = "Crosses"
    dataset = CrossResource().export()
    response = export_util(dataset, extension, object_type)

    return response
