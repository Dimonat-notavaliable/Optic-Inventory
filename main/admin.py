from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Facility)
admin.site.register(models.Muff)

admin.site.register(models.Hardware)
admin.site.register(models.HardwareType)
admin.site.register(models.Port)

admin.site.register(models.Cable)
admin.site.register(models.Module)
admin.site.register(models.Fiber)

admin.site.register(models.FOCL)
admin.site.register(models.FacilityConnection)
admin.site.register(models.MuffConnection)

admin.site.register(models.Cross)
admin.site.register(models.Adapter)
admin.site.register(models.AdapterType)

admin.site.register(models.Notification)
