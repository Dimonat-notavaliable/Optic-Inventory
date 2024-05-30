from django.shortcuts import render
from main.decorators import login_required
from main.models import Facility, FacilityConnection, Muff, MuffConnection, MuffWelding, Cable
from graphic.models import MuffScheme, MuffSchemeFOCL


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
    scheme = MuffScheme.objects.filter(muff=muff).first()
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
