from .models import Adapter, Connection, Facility, Fiber, Muff, MuffWelding


def get_connection_type(fiber, connections):
    if connections.filter(start_fiber=fiber).exists():
        connection = connections.get(start_fiber=fiber)
        other_end = connection.get_end()
    else:
        connection = connections.get(end_fiber=fiber)
        other_end = connection.get_start()

    if isinstance(other_end, Fiber):
        return "fiber", other_end
    elif isinstance(other_end, Adapter):
        return "adapter", other_end
    else:
        return "port", other_end


def get_modules_info(modules, center):
    modules_info = []
    for module in modules:
        module_info = {"object": module, "fibers": []}
        for fiber in module.fibers.all().order_by("number"):
            fiber_info = {
                "id": fiber.id,
                "hex": fiber.hex,
                "is_commutated": False,
                "connection": None,
                "connection_type": "",
            }
            if isinstance(center, Facility):
                if fiber.is_facility_commutated():
                    connections = Connection.objects.filter(facility=center)
                    fiber_info["connection_type"], fiber_info["connection"] = (
                        get_connection_type(fiber, connections)
                    )
                    fiber_info["is_commutated"] = True

            elif isinstance(center, Muff):
                if fiber.is_muff_commutated():
                    connections = MuffWelding.objects.filter(muff=center)
                    fiber_info["connection_type"], fiber_info["connection"] = (
                        get_connection_type(fiber, connections)
                    )
                    fiber_info["is_commutated"] = True
            module_info["fibers"].append(fiber_info)
        modules_info.append(module_info)
    return modules_info
