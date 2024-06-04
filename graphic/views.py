from django.shortcuts import render, get_object_or_404
from main.decorators import login_required, writer_only
from main.models import Facility, FacilityConnection, Muff, MuffConnection, MuffWelding, FOCL
from graphic.models import MuffScheme, MuffSchemeFOCL
import json
from django.http import JsonResponse


def serialize_cable(cable):
    cable_data = {
        'id': f'cable{cable.id}',
        'name': "???",
        'left': 100,
        'top': 100,
        'direction': 'down',
        'modules': []}

    for module in cable.modules.order_by('number'):
        module_data = {
            'id': f'module{module.id}',
            'color': module.hex,
            'name': f'{module.color} {module.number}',
            'fibers': []
        }
        for fiber in module.fibers.order_by('number'):
            fiber_data = {
                'id': f'fiber{fiber.id}',
                'color': fiber.hex,
            }
            module_data['fibers'].append(fiber_data)

        cable_data['modules'].append(module_data)

    return cable_data


def serialize_welding(welding):
    welding_data = {
        'start': f'fiber{welding.start_fiber.id}',
        'end': f'fiber{welding.end_fiber.id}',
        'cable_start': f'cable{welding.start_fiber.get_cable.id}',
        'cable_end': f'cable{welding.end_fiber.get_cable.id}',
    }
    return welding_data


def determine_direction(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2

    if abs(lat1 - lat2) > abs(lon1 - lon2):
        if lat1 > lat2:
            return 'up'
        else:
            return 'down'
    else:
        if lon1 > lon2:
            return 'left'
        else:
            return 'right'


@login_required
def facility_scheme(request, pk):
    facility = Facility.objects.get(pk=pk)
    connections = FacilityConnection.objects.filter(facility=facility)
    connections_data = []
    for connection in connections:
        cable = connection.focl.cable
        if cable.modules.exists():
            connection_data = serialize_cable(cable)
            other_end = connection.get_other_end()
            connection_data['name'] = other_end.name

            facility_coordinates = (facility.latitude, facility.longitude)
            other_end_coordinates = (other_end.latitude, other_end.longitude)
            direction = determine_direction(other_end_coordinates, facility_coordinates)
            connection_data['direction'] = direction

            connections_data.append(connection_data)
    title = f"Схема коммутации: {facility.name}"
    return render(request, 'scheme.html', {'title': title, 'object': facility, 'graphic': connections_data})


@login_required
def muff_scheme(request, pk):
    muff = Muff.objects.get(pk=pk)
    scheme_id = request.GET.get('scheme_id')
    if scheme_id:
        scheme = get_object_or_404(MuffScheme, pk=scheme_id, muff=muff)
    else:
        scheme = MuffScheme.objects.filter(muff=muff).latest('last_change')

    connections = MuffSchemeFOCL.objects.filter(scheme=scheme)
    connections_data = []
    for connection in connections:
        cable = connection.focl.cable
        if cable.modules.exists():
            connection_data = serialize_cable(cable)
            other_end = MuffConnection.objects.get(focl=connection.focl).get_other_end()
            connection_data['name'] = other_end.name
            connection_data['left'] = connection.coordinate_x
            connection_data['top'] = connection.coordinate_y
            connection_data['direction'] = connection.direction

            connections_data.append(connection_data)

    weldings = MuffWelding.objects.filter(muff=muff)
    weldings_data = []
    for welding in weldings:
        weldings_data.append(serialize_welding(welding))

    title = f"Схема коммутации: {muff.name}"
    return render(request, 'scheme.html', {'title': title, 'object': muff,
                                           'connections': connections_data, 'weldings': weldings_data})


@login_required
def get_muff_schemes(request, pk):
    muff = Muff.objects.get(pk=pk)
    schemes = MuffScheme.objects.filter(muff=muff).order_by('-last_change')
    schemes_data = [
        {
            'id': scheme.id,
            'last_change': scheme.last_change.strftime('%d.%m.%Y %H:%M:%S')
        }
        for scheme in schemes
    ]
    return JsonResponse({'schemes': schemes_data})


@writer_only
def save_muff_scheme(request, pk):
    try:
        # Получаем муфту и её схему
        muff = Muff.objects.get(pk=pk)

        # Парсим данные из запроса
        data = json.loads(request.body)

        # Получаем все схемы муфты, отсортированные по дате создания
        muff_schemes = MuffScheme.objects.filter(muff=muff).order_by('last_change')

        # Проверяем, если количество схем превышает пять, удаляем самую старую
        if muff_schemes.count() >= 5:
            oldest_scheme = muff_schemes.first()
            oldest_scheme.delete()

        new_scheme = MuffScheme.objects.create(muff=muff)

        for connection_data in data.get('connections', []):
            MuffSchemeFOCL.objects.create(
                scheme=new_scheme,
                focl=FOCL.objects.get(cable_id=connection_data['id']),
                coordinate_x=connection_data['left'],
                coordinate_y=connection_data['top'],
                direction=connection_data['direction']
            )

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
