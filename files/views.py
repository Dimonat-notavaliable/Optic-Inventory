import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from tablib import Dataset

from main.decorators import login_required, writer_only
from main.models import FOCL, Cross, Facility, Hardware, Muff

from . import admin
from .forms import ImportForm


def export_util(dataset, dataset_type, object_description):
    export_time = datetime.datetime.now().strftime("%d-%m-%Y(%H-%M)")
    if dataset_type == "csv":
        response = HttpResponse(dataset.csv, content_type="application/csv")
        response["Content-Disposition"] = (
            f"attachment; filename=OpticInventory_{object_description}_{export_time}.csv"
        )
    else:
        response = HttpResponse(dataset.xlsx, content_type="application/excel")
        response["Content-Disposition"] = (
            f"attachment; filename=OpticInventory_{object_description}_{export_time}.xlsx"
        )
    return response


def import_util(request, resource, headers, import_url, success_url):
    file = request.FILES["file"]
    dataset_type = file.name.split(".")[-1]

    dataset = Dataset(headers=headers)
    dataset.load(file.read(), format=dataset_type)

    result = resource.import_data(
        dataset, dry_run=True, raise_errors=True
    )  # Dry run to check for errors

    if not result.has_errors():
        resource.import_data(dataset, dry_run=False)  # Actually import now
        messages.success(request, "Импорт завершен.")
        return success_url
    else:
        messages.error(
            request,
            "Импорт не удался. Пожалуйста, проверьте формат файла и целостность данных.",
        )
        return import_url


@login_required
def export_hardware(request, extension):
    object_type = "Hardware"
    dataset = admin.HardwareExportResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_one_hardware(request, extension, pk):
    queryset = Hardware.objects.filter(id=pk)
    object_name = f"Hardware_{pk}"
    dataset = admin.HardwareExportResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@writer_only
def import_hardware(request):
    headers_file = "xlsx/OpticInventory_Заголовки_Оборудование.xlsx"
    title = "Импорт оборудования"
    redirect_url = "import_hardware"
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = admin.HardwareImportResource()
            headers = [
                "id",
                "facility",
                "floor",
                "marking",
                "type",
                "IP",
                "MAC",
                "port_count",
            ]
            redirect_url = import_util(
                request,
                resource,
                headers,
                import_url="import_hardware",
                success_url="many_hardware",
            )
        return redirect(redirect_url)
    else:
        form = ImportForm()
    return render(
        request,
        "import.html",
        {"title": title, "form": form, "headers_file": headers_file},
    )


@login_required
def export_facilities(request, extension):
    object_type = "Facilities"
    dataset = admin.FacilityExportResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_facility(request, extension, pk):
    queryset = Facility.objects.filter(id=pk)
    object_name = f"Facility_{pk}"
    dataset = admin.FacilityExportResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@writer_only
def import_facilities(request):
    headers_file = "xlsx/OpticInventory_Заголовки_СооруженияСвязи.xlsx"
    title = "Импорт сооружений связи"
    redirect_url = "import_facilities"
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = admin.FacilityImportResource()
            headers = ["id", "name", "floor_count", "latitude", "longitude"]
            redirect_url = import_util(
                request,
                resource,
                headers,
                import_url="import_facilities",
                success_url="facilities",
            )
        return redirect(redirect_url)
    else:
        form = ImportForm()
    return render(
        request,
        "import.html",
        {"title": title, "form": form, "headers_file": headers_file},
    )


@login_required
def export_muffs(request, extension):
    object_type = "Muffs"
    dataset = admin.MuffExportResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_muff(request, extension, pk):
    queryset = Muff.objects.filter(id=pk)
    object_name = f"Muff_{pk}"
    dataset = admin.MuffExportResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@writer_only
def import_muffs(request):
    headers_file = "xlsx/OpticInventory_Заголовки_Муфты.xlsx"
    title = "Импорт муфт"
    redirect_url = "import_muffs"
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = admin.MuffImportResource()
            headers = ["id", "name", "capacity", "latitude", "longitude"]
            redirect_url = import_util(
                request,
                resource,
                headers,
                import_url="import_muffs",
                success_url="muffs",
            )
        return redirect(redirect_url)
    else:
        form = ImportForm()
    return render(
        request,
        "import.html",
        {"title": title, "form": form, "headers_file": headers_file},
    )


@login_required
def export_focls(request, extension):
    object_type = "FOCLs"
    dataset = admin.FOCLExportResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_focl(request, extension, pk):
    queryset = FOCL.objects.filter(id=pk)
    object_name = f"FOCL_{pk}"
    dataset = admin.FOCLExportResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@writer_only
def import_focls(request):
    headers_file = "xlsx/OpticInventory_Заголовки_ВОЛС.xlsx"
    title = "Импорт линий связи"
    redirect_url = "import_focls"
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = admin.FOCLImportResource()
            headers = [
                "id",
                "start_type",
                "start_name",
                "end_type",
                "end_name",
                "cable",
                "cable_length",
                "fiber_length",
            ]
            redirect_url = import_util(
                request,
                resource,
                headers,
                import_url="import_focls",
                success_url="focls",
            )
        return redirect(redirect_url)
    else:
        form = ImportForm()
    return render(
        request,
        "import.html",
        {"title": title, "form": form, "headers_file": headers_file},
    )


@login_required
def export_crosses(request, extension):
    object_type = "Crosses"
    dataset = admin.CrossExportResource().export()
    response = export_util(dataset, extension, object_type)

    return response


@login_required
def export_cross(request, extension, pk):
    queryset = Cross.objects.filter(id=pk)
    object_name = f"Cross_{pk}"
    dataset = admin.CrossExportResource().export(queryset)
    response = export_util(dataset, extension, object_name)

    return response


@writer_only
def import_crosses(request):
    headers_file = "xlsx/OpticInventory_Заголовки_Кроссы.xlsx"
    title = "Импорт кроссов"
    redirect_url = "import_crosses"
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            resource = admin.CrossImportResource()
            headers = [
                "id",
                "facility",
                "floor",
                "adapter_count",
                "linear_type",
                "station_type",
            ]
            redirect_url = import_util(
                request,
                resource,
                headers,
                import_url="import_crosses",
                success_url="crosses",
            )
        return redirect(redirect_url)
    else:
        form = ImportForm()
    return render(
        request,
        "import.html",
        {"title": title, "form": form, "headers_file": headers_file},
    )
