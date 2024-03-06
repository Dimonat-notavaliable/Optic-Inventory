from django.contrib import admin
from .models import Hardware, Port, Facility, Cable, Module, Fiber
# Register your models here.
admin.site.register(Facility)

admin.site.register(Hardware)
admin.site.register(Port)

admin.site.register(Cable)
admin.site.register(Module)
admin.site.register(Fiber)