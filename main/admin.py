from django.contrib import admin
from .models import Hardware, Port, Facility, Cable, Module, Fiber, FOCL, Muff, FacilityConnection, MuffConnection
# Register your models here.
admin.site.register(Facility)
admin.site.register(Muff)

admin.site.register(Hardware)
admin.site.register(Port)

admin.site.register(Cable)
admin.site.register(Module)
admin.site.register(Fiber)

admin.site.register(FOCL)
admin.site.register(FacilityConnection)
admin.site.register(MuffConnection)