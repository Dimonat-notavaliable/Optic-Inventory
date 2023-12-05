from django.contrib import admin
from .models import Hardware, Port, Facility
# Register your models here.
admin.site.register(Hardware)
admin.site.register(Facility)
admin.site.register(Port)
