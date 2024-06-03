from import_export import fields, resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from main.models import Hardware, HardwareType, Facility, Muff, FOCL, Cross


class HardwareExportResource(resources.ModelResource):
    marking = Field(attribute='marking', column_name='Наименование')
    type_marking = Field(attribute='type__marking', column_name='Тип')
    facility_name = Field(attribute='facility__name', column_name='Расположение')
    port_count = Field(attribute='port_count', column_name='Количество портов')
    floor = Field(attribute='floor', column_name='Этаж расположения')
    IP = Field(attribute='IP', column_name='IP-адрес')
    MAC = Field(attribute='MAC', column_name='MAC-адрес')

    class Meta:
        model = Hardware
        exclude = ('id', 'facility', 'type',)
        export_order = ('facility_name', 'floor', 'marking', 'type_marking', 'IP', 'MAC', 'port_count')


class HardwareImportResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Идентификатор')
    facility = fields.Field(
        column_name='Расположение',
        attribute='facility',
        widget=ForeignKeyWidget(Facility, field='name'))
    floor = Field(attribute='floor', column_name='Этаж расположения')
    marking = Field(attribute='marking', column_name='Наименование')
    type = fields.Field(
        column_name='Тип',
        attribute='type',
        widget=ForeignKeyWidget(HardwareType, field='marking'))
    IP = Field(attribute='IP', column_name='IP-адрес')
    MAC = Field(attribute='MAC', column_name='MAC-адрес')
    port_count = Field(attribute='port_count', column_name='Количество портов')

    class Meta:
        model = Hardware


class FacilityExportResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Наименование')
    latitude = Field(attribute='latitude', column_name='Широта')
    longitude = Field(attribute='longitude', column_name='Долгота')
    floor_count = Field(attribute='floor_count', column_name='Количество этажей')

    class Meta:
        model = Facility
        exclude = ('id',)
        export_order = ('name', 'floor_count', 'latitude', 'longitude')


class FacilityImportResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Идентификатор')
    name = Field(attribute='name', column_name='Наименование')
    latitude = Field(attribute='latitude', column_name='Широта')
    longitude = Field(attribute='longitude', column_name='Долгота')
    floor_count = Field(attribute='floor_count', column_name='Количество этажей')

    class Meta:
        model = Facility


class MuffExportResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Наименование')
    latitude = Field(attribute='latitude', column_name='Широта')
    longitude = Field(attribute='longitude', column_name='Долгота')
    capacity = Field(attribute='capacity', column_name='Вместимость')

    class Meta:
        model = Muff
        exclude = ('id',)
        export_order = ('name', 'capacity', 'latitude', 'longitude')


class MuffImportResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Идентификатор')
    name = Field(attribute='name', column_name='Наименование')
    latitude = Field(attribute='latitude', column_name='Широта')
    longitude = Field(attribute='longitude', column_name='Долгота')
    capacity = Field(attribute='capacity', column_name='Вместимость')

    class Meta:
        model = Muff


class FOCLResource(resources.ModelResource):
    cable = Field(attribute='cable__marking', column_name='Кабель')
    cable_length = Field(attribute='cable_length', column_name='Длина по кабелю')
    fiber_length = Field(attribute='fiber_length', column_name='Длина по волокну')
    start_point = Field(column_name='Начальная точка')
    end_point = Field(column_name='Конечная точка')

    def dehydrate_cable(self, focl):
        return focl.cable.__str__()

    def dehydrate_start_point(self, focl):
        start_point = focl.get_start()
        return start_point.name

    def dehydrate_end_point(self, focl):
        end_point = focl.get_end()
        return end_point.name

    class Meta:
        model = FOCL
        exclude = ('id',)
        export_order = ('start_point', 'end_point', 'cable', 'cable_length', 'fiber_length')


class CrossResource(resources.ModelResource):
    facility_name = Field(attribute='facility__name', column_name='Расположение')
    floor = Field(attribute='floor', column_name='Этаж расположения')
    adapter_count = Field(attribute='adapter_count', column_name='Количество адаптеров')
    linear_type = Field(attribute='linear_type__marking', column_name='Тип линейных адаптеров')
    station_type = Field(attribute='station_type__marking', column_name='Тип станционных адаптеров')

    class Meta:
        model = Cross
        exclude = ('id', 'facility',)
        export_order = ('facility_name', 'floor', 'adapter_count', 'linear_type', 'station_type')



