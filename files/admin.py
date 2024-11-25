from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from main.models import (Hardware, HardwareType, Facility, FacilityConnection, Muff, MuffConnection, FOCL, Cross,
                         AdapterType, Cable)


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
    facility = Field(
        column_name='Расположение',
        attribute='facility',
        widget=ForeignKeyWidget(Facility, field='name'))
    floor = Field(attribute='floor', column_name='Этаж расположения')
    marking = Field(attribute='marking', column_name='Наименование')
    type = Field(
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


class FOCLExportResource(resources.ModelResource):
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


class FOCLImportResource(resources.ModelResource):

    cable = Field(
        column_name='Кабель',
        attribute='cable',
        widget=ForeignKeyWidget(Cable, field='marking')
    )

    start_type = Field(column_name='Тип начальной точки')
    start_name = Field(column_name='Начальная точка')
    end_type = Field(column_name='Тип конечной точки')
    end_name = Field(column_name='Конечная точка')

    cable_length = Field(attribute='cable_length', column_name='Длина по кабелю')
    fiber_length = Field(attribute='fiber_length', column_name='Длина по волокну')

    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        instance = row_result.instance
        if instance:
            start_type = row.get('Тип начальной точки').strip().lower()
            start_name = row.get('Начальная точка')
            end_type = row.get('Тип конечной точки').strip().lower()
            end_name = row.get('Конечная точка')

            try:
                if start_type == 'сооружение связи':
                    instance = row_result.instance
                    start_facility = Facility.objects.get(name=start_name)
                    start_connection = FacilityConnection(focl=instance, facility=start_facility, is_start=True)
                    start_connection.save()

                elif start_type == 'муфта':
                    start_muff = Muff.objects.get(name=start_name)
                    start_connection = MuffConnection(focl=instance, muff=start_muff, is_start=True)
                    start_connection.save()

                if end_type == 'сооружение связи':
                    end_facility = Facility.objects.get(name=end_name)
                    end_connection = FacilityConnection(focl=instance, facility=end_facility, is_start=False)
                    end_connection.save()

                elif end_type == 'муфта':
                    end_muff = Muff.objects.get(name=end_name)
                    end_connection = MuffConnection(focl=instance, muff=end_muff, is_start=False)
                    end_connection.save()

            except Facility.DoesNotExist:
                print(
                    f"Сооружения связи '{start_name if start_type == 'сооружение связи' else end_name}' не существует.")
            except Muff.DoesNotExist:
                print(f"Муфты '{start_name if start_type == 'муфта' else end_name}' не существует.")

    class Meta:
        model = FOCL
        store_instance = True
        fields = ('id', 'start_type', 'start_name', 'end_type', 'end_name',
                  'cable', 'cable_length', 'fiber_length')


class CrossExportResource(resources.ModelResource):
    facility_name = Field(attribute='facility__name', column_name='Расположение')
    floor = Field(attribute='floor', column_name='Этаж расположения')
    adapter_count = Field(attribute='adapter_count', column_name='Количество адаптеров')
    linear_type = Field(attribute='linear_type__marking', column_name='Тип линейных адаптеров')
    station_type = Field(attribute='station_type__marking', column_name='Тип станционных адаптеров')

    class Meta:
        model = Cross
        exclude = ('id', 'facility',)
        export_order = ('facility_name', 'floor', 'adapter_count', 'linear_type', 'station_type')


class CrossImportResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Идентификатор')
    facility = Field(
        column_name='Расположение',
        attribute='facility',
        widget=ForeignKeyWidget(Facility, field='name')
    )
    floor = Field(attribute='floor', column_name='Этаж расположения')
    adapter_count = Field(attribute='adapter_count', column_name='Количество адаптеров')
    linear_type = Field(
        column_name='Тип линейных адаптеров',
        attribute='linear_type',
        widget=ForeignKeyWidget(AdapterType, field='marking')
    )
    station_type = Field(
        column_name='Тип станционных адаптеров',
        attribute='station_type',
        widget=ForeignKeyWidget(AdapterType, field='marking')
    )

    class Meta:
        model = Cross
