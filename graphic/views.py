import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from main.decorators import login_required, writer_only
from main.models import (FOCL, Adapter, Connection, Cross, Facility,
                         FacilityConnection, Fiber, Hardware, Muff,
                         MuffConnection, MuffWelding, Port)

from graphic.models import (FacilityScheme, FacilitySchemeObject, MuffScheme,
                            MuffSchemeFOCL, SchemeObjectType)


def serialize_cable(cable):
    cable_data = {
        "id": f"cable{cable.id}",
        "name": "???",
        "left": 100,
        "top": 100,
        "direction": "down",
        "modules": [],
    }

    for module in cable.modules.order_by("number"):
        module_data = {
            "id": f"module{module.id}",
            "color": module.hex,
            "name": f"{module.color} {module.number}",
            "fibers": [],
        }
        for fiber in module.fibers.order_by("number"):
            fiber_data = {
                "id": f"fiber{fiber.id}",
                "color": fiber.hex,
            }
            module_data["fibers"].append(fiber_data)

        cable_data["modules"].append(module_data)

    return cable_data


def serialize_hardware(hardware):
    hardware_data = {
        "id": f"hardware{hardware.id}",
        "marking": hardware.marking,
        "left": 100,
        "top": 100,
        "direction": "left",
        "ports": [],
    }

    for port in hardware.ports.order_by("number"):
        port_data = {
            "id": f"port{port.id}",
        }
        hardware_data["ports"].append(port_data)

    return hardware_data


def serialize_cross(cross):
    cross_data = {
        "id": f"cross{cross.id}",
        "linear_type": cross.linear_type.marking,
        "station_type": cross.station_type.marking,
        "left": 100,
        "top": 100,
        "direction": "right",
        "linear_adapters": [],
        "station_adapters": [],
    }

    for adapter in cross.adapters.order_by("number"):
        adapter_data = {
            "id": f"adapter{adapter.id}",
        }
        if adapter.is_linear:
            cross_data["linear_adapters"].append(adapter_data)
        else:
            cross_data["station_adapters"].append(adapter_data)

    return cross_data


def serialize_welding(welding):
    welding_data = {
        "start": f"fiber{welding.start_fiber.id}",
        "end": f"fiber{welding.end_fiber.id}",
        "object_start": f"cable{welding.start_fiber.get_cable.id}",
        "object_end": f"cable{welding.end_fiber.get_cable.id}",
    }
    return welding_data


def serialize_connection(connection):
    connection_data = {
        "start": "",
        "end": "",
        "object_start": "",
        "object_end": "",
    }
    start = connection.get_start()
    end = connection.get_end()
    for word in ["start", "end"]:
        if word == "start":
            entity = start
        else:
            entity = end
        object_word = "object_" + word
        if isinstance(entity, Adapter):
            connection_data[word] = f"adapter{entity.id}"
            connection_data[object_word] = f"cross{entity.cross.id}"
        elif isinstance(entity, Port):
            connection_data[word] = f"port{entity.id}"
            connection_data[object_word] = f"hardware{entity.hardware.id}"
        elif isinstance(entity, Fiber):
            connection_data[word] = f"fiber{entity.id}"
            connection_data[object_word] = f"cable{entity.get_cable.id}"
    return connection_data


def determine_direction(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2

    if abs(lat1 - lat2) > abs(lon1 - lon2):
        if lat1 > lat2:
            return "up"
        else:
            return "down"
    else:
        if lon1 > lon2:
            return "left"
        else:
            return "right"


@login_required
def facility_scheme(request, pk):
    facility = Facility.objects.get(pk=pk)
    title = f"Схема коммутации: {facility.name}"

    scheme_id = request.GET.get("scheme_id")
    if scheme_id:
        scheme = get_object_or_404(FacilityScheme, pk=scheme_id, facility=facility)
    elif FacilityScheme.objects.filter(facility=facility).exists():
        scheme = FacilityScheme.objects.filter(facility=facility).latest("last_change")
    else:
        return render(request, "scheme.html", {"title": title, "object": facility})

    objects = FacilitySchemeObject.objects.filter(scheme=scheme)
    cables = objects.filter(object_type=1)
    cables_data = []
    for cable in cables:
        line = FOCL.objects.get(pk=cable.object_id)
        cable_object = line.cable
        if cable_object.modules.exists():
            cable_data = serialize_cable(cable_object)
            other_end = FacilityConnection.objects.get(focl=line).get_other_end()
            cable_data["name"] = other_end.name
            cable_data["left"] = cable.coordinate_x
            cable_data["top"] = cable.coordinate_y
            cable_data["direction"] = cable.direction

            cables_data.append(cable_data)

    many_hardware_data = []
    many_hardware = objects.filter(object_type=2)
    for hardware in many_hardware:
        hardware_object = Hardware.objects.get(pk=hardware.object_id)
        hardware_data = serialize_hardware(hardware_object)
        hardware_data["left"] = hardware.coordinate_x
        hardware_data["top"] = hardware.coordinate_y
        hardware_data["direction"] = hardware.direction

        many_hardware_data.append(hardware_data)

    crosses_data = []
    crosses = objects.filter(object_type=3)
    for cross in crosses:
        cross_object = Cross.objects.get(pk=cross.object_id)
        cross_data = serialize_cross(cross_object)
        cross_data["left"] = cross.coordinate_x
        cross_data["top"] = cross.coordinate_y
        cross_data["direction"] = cross.direction

        crosses_data.append(cross_data)

    connections = Connection.objects.filter(facility=facility)
    connections_data = []
    for connection in connections:
        connections_data.append(serialize_connection(connection))

    return render(
        request,
        "scheme.html",
        {
            "title": title,
            "object": facility,
            "cables": cables_data,
            "crosses": crosses_data,
            "hardware": many_hardware_data,
            "connections": connections_data,
        },
    )


@login_required
def get_facility_schemes(request, pk):
    facility = Facility.objects.get(pk=pk)
    schemes = FacilityScheme.objects.filter(facility=facility).order_by("-last_change")
    schemes_data = [
        {
            "id": scheme.id,
            "last_change": (scheme.last_change + timedelta(hours=7)).strftime(
                "%d.%m.%Y %H:%M:%S"
            ),
        }
        for scheme in schemes
    ]
    return JsonResponse({"schemes": schemes_data})


@writer_only
def save_facility_scheme(request, pk):
    try:
        # Получаем муфту и её схему
        facility = Facility.objects.get(pk=pk)

        # Парсим данные из запроса
        data = json.loads(request.body)

        # Получаем все схемы муфты, отсортированные по дате создания
        facility_schemes = FacilityScheme.objects.filter(facility=facility).order_by(
            "last_change"
        )

        # Проверяем, если количество схем превышает пять, удаляем самую старую
        if facility_schemes.count() >= 5:
            oldest_scheme = facility_schemes.first()
            oldest_scheme.delete()

        new_scheme = FacilityScheme.objects.create(facility=facility)

        for cable_data in data.get("cables", []):
            FacilitySchemeObject.objects.create(
                scheme=new_scheme,
                object_id=cable_data["id"],
                object_type=SchemeObjectType.objects.get(pk=1),
                coordinate_x=cable_data["left"],
                coordinate_y=cable_data["top"],
                direction=cable_data["direction"],
            )

        for hardware_data in data.get("hardware", []):
            FacilitySchemeObject.objects.create(
                scheme=new_scheme,
                object_id=hardware_data["id"],
                object_type=SchemeObjectType.objects.get(pk=2),
                coordinate_x=hardware_data["left"],
                coordinate_y=hardware_data["top"],
                direction=hardware_data["direction"],
            )

        for cross_data in data.get("crosses", []):
            FacilitySchemeObject.objects.create(
                scheme=new_scheme,
                object_id=cross_data["id"],
                object_type=SchemeObjectType.objects.get(pk=3),
                coordinate_x=cross_data["left"],
                coordinate_y=cross_data["top"],
                direction=cross_data["direction"],
            )

        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
def muff_scheme(request, pk):
    muff = Muff.objects.get(pk=pk)
    title = f"Схема коммутации: {muff.name}"

    scheme_id = request.GET.get("scheme_id")
    if scheme_id:
        scheme = get_object_or_404(MuffScheme, pk=scheme_id, muff=muff)
    elif MuffScheme.objects.filter(muff=muff).exists():
        scheme = MuffScheme.objects.filter(muff=muff).latest("last_change")
    else:
        return render(request, "scheme.html", {"title": title, "object": muff})

    cables = MuffSchemeFOCL.objects.filter(scheme=scheme)
    cables_data = []
    for cable in cables:
        cable_object = cable.focl.cable
        if cable_object.modules.exists():
            cable_data = serialize_cable(cable_object)
            other_end = MuffConnection.objects.get(focl=cable.focl).get_other_end()
            cable_data["name"] = other_end.name
            cable_data["left"] = cable.coordinate_x
            cable_data["top"] = cable.coordinate_y
            cable_data["direction"] = cable.direction

            cables_data.append(cable_data)

    weldings = MuffWelding.objects.filter(muff=muff)
    weldings_data = []
    for welding in weldings:
        weldings_data.append(serialize_welding(welding))

    return render(
        request,
        "scheme.html",
        {
            "title": title,
            "object": muff,
            "cables": cables_data,
            "connections": weldings_data,
        },
    )


@login_required
def get_muff_schemes(request, pk):
    muff = Muff.objects.get(pk=pk)
    schemes = MuffScheme.objects.filter(muff=muff).order_by("-last_change")
    schemes_data = [
        {
            "id": scheme.id,
            "last_change": scheme.last_change.strftime("%d.%m.%Y %H:%M:%S"),
        }
        for scheme in schemes
    ]
    return JsonResponse({"schemes": schemes_data})


@writer_only
def save_muff_scheme(request, pk):
    try:
        # Получаем муфту и её схему
        muff = Muff.objects.get(pk=pk)

        # Парсим данные из запроса
        data = json.loads(request.body)

        # Получаем все схемы муфты, отсортированные по дате создания
        muff_schemes = MuffScheme.objects.filter(muff=muff).order_by("last_change")

        # Проверяем, если количество схем превышает пять, удаляем самую старую
        if muff_schemes.count() >= 5:
            oldest_scheme = muff_schemes.first()
            oldest_scheme.delete()

        new_scheme = MuffScheme.objects.create(muff=muff)

        for cable_data in data.get("cables", []):
            MuffSchemeFOCL.objects.create(
                scheme=new_scheme,
                focl=FOCL.objects.get(cable_id=cable_data["id"]),
                coordinate_x=cable_data["left"],
                coordinate_y=cable_data["top"],
                direction=cable_data["direction"],
            )

        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
