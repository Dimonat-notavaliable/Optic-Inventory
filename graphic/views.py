from django.shortcuts import render
from main.decorators import login_required
from main.models import Facility, Muff


@login_required
def facility_scheme(request, pk):
    facility = Facility.objects.get(pk=pk)
    title = f"Схема коммутации: {facility.name}"
    return render(request, 'scheme.html', {'title': title, 'object': facility})


@login_required
def muff_scheme(request, pk):
    muff = Muff.objects.get(pk=pk)
    title = f"Схема коммутации: {muff.name}"
    return render(request, 'scheme.html', {'title': title, 'object': muff})
