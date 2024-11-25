from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.MuffScheme)
admin.site.register(models.MuffSchemeFOCL)

admin.site.register(models.FacilityScheme)
admin.site.register(models.SchemeObjectType)
admin.site.register(models.FacilitySchemeObject)
