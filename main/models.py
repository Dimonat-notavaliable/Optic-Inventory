from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model


# Узел связи
class CommunicationCenter(models.Model):
    name = models.CharField(_("Наименование"), blank=False)
    latitude = models.DecimalField(_("Широта"), max_digits=9, decimal_places=6, blank=False)
    longitude = models.DecimalField(_("Долгота"), max_digits=9, decimal_places=6, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# Сооружение связи
class Facility(CommunicationCenter):
    floor_count = models.IntegerField(_("Количество этажей"), blank=False, default=1,
                                      validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Сооружение связи'
        verbose_name_plural = 'Сооружения связи'

    @staticmethod
    def class_name():
        return "Facility"


# Муфта
class Muff(CommunicationCenter):
    capacity = models.IntegerField(_("Вместимость"), blank=False, default=64,
                                   validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Муфта'
        verbose_name_plural = 'Муфты'

    @staticmethod
    def class_name():
        return "Muff"


class HardwareType(models.Model):
    marking = models.CharField(_("Наименование"), blank=False, unique=True)

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'

    def __str__(self):
        return f'{self.marking}'


# Сетевое оборудование (маршрутизаторы, IP-телефоны, коммутаторы и т.д.)
class Hardware(models.Model):
    marking = models.CharField(_("Наименование"), blank=False)
    type = models.ForeignKey(HardwareType, on_delete=models.CASCADE, related_name='hardware', blank=False)
    port_count = models.IntegerField(_("Количество портов"), default=0, blank=False)
    floor = models.IntegerField(_("Этаж расположения"), blank=False, default=1,
                                validators=[MinValueValidator(1)])
    IP = models.GenericIPAddressField(_("IP-адрес"), protocol="both", blank=True, null=True)
    MAC = models.CharField(_("MAC-адрес"), blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, related_name='hardware', blank=True, null=True)

    class Meta:
        verbose_name = 'Сетевое оборудование'
        verbose_name_plural = 'Сетевое оборудование'

    def count_free(self):
        count = 0
        for port in self.ports.all():
            if not port.is_commutated():
                count += 1
        return count

    def __str__(self):
        return f'{self.marking} #{self.id}'


# Порт сетевого оборудования
class Port(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name='ports', blank=False)

    class Meta:
        verbose_name = 'Порт оборудования'
        verbose_name_plural = 'Порты оборудования'

    def is_commutated(self):
        if self.start_connections.exists() or self.end_connections.exists():
            return True
        else:
            return False

    def get_connection(self):
        if self.is_commutated:
            if self.start_connections.exists():
                connection = self.start_connections.first()
            else:
                connection = self.end_connections.first()
            return connection
        else:
            return None

    def __str__(self):
        return f'{self.hardware.marking} #{self.hardware.id}: Порт {self.number}'


def create_hardware_ports(instance, **kwargs):
    for number in range(instance.port_count):
        port, _ = Port.objects.get_or_create(number=number + 1, hardware=instance)


models.signals.post_save.connect(create_hardware_ports, sender=Hardware, dispatch_uid='create_hardware_ports')


class AdapterType(models.Model):
    marking = models.CharField(_("Наименование"), blank=False, unique=True)

    class Meta:
        verbose_name = 'Тип адаптера'
        verbose_name_plural = 'Типы адаптеров'

    def __str__(self):
        return f'Тип {self.marking}'


# Оптический кросс
class Cross(models.Model):
    floor = models.IntegerField(_("Этаж расположения"), blank=False, default=1,
                                validators=[MinValueValidator(1)])
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, related_name='crosses', blank=True, null=True)
    linear_type = models.ForeignKey(AdapterType, on_delete=models.CASCADE, related_name='linear', blank=False)
    station_type = models.ForeignKey(AdapterType, on_delete=models.CASCADE, related_name='station', blank=False)
    adapter_count = models.IntegerField(_("Количество адаптеров"), default=0, blank=False)

    class Meta:
        verbose_name = 'Оптический кросс'
        verbose_name_plural = 'Оптические кроссы'

    def __str__(self):
        return f'Кросс #{self.id}'


# Адаптер оптического кросса
class Adapter(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    cross = models.ForeignKey(Cross, on_delete=models.CASCADE, related_name='adapters', blank=False)
    type = models.ForeignKey(AdapterType, on_delete=models.CASCADE, related_name='adapters', blank=False)
    is_linear = models.BooleanField(_("Линейная сторона"), blank=False)

    class Meta:
        verbose_name = 'Адаптер кросса'
        verbose_name_plural = 'Адаптеры кросса'

    def is_commutated(self):
        if self.start_connections.exists() or self.end_connections.exists():
            return True
        else:
            return False

    def get_connection(self):
        if self.is_commutated:
            if self.start_connections.exists():
                connection = self.start_connections.first()
            else:
                connection = self.end_connections.first()
            return connection
        else:
            return None

    def __str__(self):
        type = "линейный" if self.is_linear else "станционный"
        return f'{self.cross}: Адаптер {self.number} {type} {self.type}'


def create_cross_adapters(instance, **kwargs):
    for number in range(instance.adapter_count):
        linear_adapter, _ = Adapter.objects.get_or_create(number=number + 1, cross=instance,
                                                          type=instance.linear_type, is_linear=True)
        station_adapter, _ = Adapter.objects.get_or_create(number=number + 1, cross=instance,
                                                           type=instance.station_type, is_linear=False)


models.signals.post_save.connect(create_cross_adapters, sender=Cross, dispatch_uid='create_cross_adapters')


class Cable(models.Model):
    producer = models.CharField(_("Производитель"), blank=False)
    marking = models.CharField(_("Маркировка"), blank=False)
    map_hex = ColorField(_("Цвет на карте"), default='#FFFFFF')

    class Meta:
        verbose_name = 'Кабель'
        verbose_name_plural = 'Кабели'

    def __str__(self):
        return f'{self.producer} {self.marking}'

    def get_fiber_count(self):
        count = 0
        for module in self.modules.all():
            count += module.get_fiber_count()
        return count


class Module(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, related_name='modules', blank=False)
    color = models.CharField(_("Цвет"), blank=False, default="Белый")
    hex = ColorField(_("Отображаемый цвет"), default='#FFFFFF')

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return f'{self.cable}: Модуль №{self.number}'

    def get_fiber_count(self):
        return len(self.fibers.all())


class Fiber(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='fibers', blank=False)
    color = models.CharField(_("Цвет"), blank=False, default="Белый")
    hex = ColorField(_("Отображаемый цвет"), default='#FFFFFF')

    class Meta:
        verbose_name = 'Волокно'
        verbose_name_plural = 'Волокна'

    def __str__(self):
        return f'{self.module}: Волокно №{self.number}'

    @property
    def get_cable(self):
        return self.module.cable

    def is_facility_commutated(self):
        if self.start_connections.exists() or self.end_connections.exists():
            return True
        else:
            return False

    def is_muff_commutated(self):
        if self.start_muff_connections.exists() or self.end_muff_connections.exists():
            return True
        else:
            return False


class FOCL(models.Model):
    cable = models.OneToOneField(Cable, on_delete=models.CASCADE, related_name='focl', blank=False)
    cable_length = models.DecimalField(_("Длина по кабелю"), max_digits=9, decimal_places=2, blank=False)
    fiber_length = models.DecimalField(_("Длина по волокну"), max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Линия связи'
        verbose_name_plural = 'Линии связи'

    def __str__(self):
        return f'Линия связи: {self.get_start()} - {self.get_end()}'

    def get_start(self):
        if self.connection_muff.filter(is_start=True):
            start = self.connection_muff.filter(is_start=True)[0].muff
        elif self.connection_facility.filter(is_start=True):
            start = self.connection_facility.filter(is_start=True)[0].facility
        else:
            start = None
        return start

    def get_end(self):
        if self.connection_muff.filter(is_start=False):
            end = self.connection_muff.filter(is_start=False)[0].muff
        elif self.connection_facility.filter(is_start=False):
            end = self.connection_facility.filter(is_start=False)[0].facility
        else:
            end = None
        return end


class FacilityConnection(models.Model):
    focl = models.ForeignKey(FOCL, on_delete=models.CASCADE, related_name='connection_facility', blank=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='connection', blank=False)
    is_start = models.BooleanField(_("Начало"), blank=False)

    class Meta:
        verbose_name = 'Следование через сооружение'
        verbose_name_plural = 'Следования через сооружение'

    def __str__(self):
        return f'{self.focl} через {self.facility}'

    def get_other_end(self):
        muff_connection = MuffConnection.objects.filter(focl=self.focl)
        if muff_connection.exists():
            other_end = muff_connection.first().muff
        else:
            facility_connection = FacilityConnection.objects.filter(focl=self.focl).exclude(facility=self.facility)
            other_end = facility_connection.first().facility
        return other_end


class MuffConnection(models.Model):
    focl = models.ForeignKey(FOCL, on_delete=models.CASCADE, related_name='connection_muff', blank=False)
    muff = models.ForeignKey(Muff, on_delete=models.CASCADE, related_name='connection', blank=False)
    is_start = models.BooleanField(_("Начало"), blank=False)

    class Meta:
        verbose_name = 'Следование через муфту'
        verbose_name_plural = 'Следования через муфту'

    def __str__(self):
        return f'{self.focl} через {self.muff}'

    def get_other_end(self):
        facility_connection = FacilityConnection.objects.filter(focl=self.focl)
        if facility_connection.exists():
            other_end = facility_connection.first().facility
        else:
            muff_connection = MuffConnection.objects.filter(focl=self.focl).exclude(muff=self.muff)
            other_end = muff_connection.first().muff
        return other_end


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'Действие от {self.user.get_full_name}'


class Connection(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='connections', blank=False)
    start_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='start_connections',
                                   blank=True, null=True)
    start_adapter = models.ForeignKey(Adapter, on_delete=models.CASCADE, related_name='start_connections',
                                      blank=True, null=True)
    start_fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE, related_name='start_connections',
                                    blank=True, null=True)
    end_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='end_connections',
                                 blank=True, null=True)
    end_adapter = models.ForeignKey(Adapter, on_delete=models.CASCADE, related_name='end_connections',
                                    blank=True, null=True)
    end_fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE, related_name='end_connections',
                                  blank=True, null=True)

    def get_start(self):
        if self.start_port:
            return self.start_port
        elif self.start_adapter:
            return self.start_adapter
        else:
            return self.start_fiber

    def get_end(self):
        if self.end_port:
            return self.end_port
        elif self.end_adapter:
            return self.end_adapter
        else:
            return self.end_fiber

    class Meta:
        verbose_name = 'Соединение'
        verbose_name_plural = 'Соединения'

    def __str__(self):
        return f'Соединение №{self.id}'


class MuffWelding(models.Model):
    muff = models.ForeignKey(Muff, on_delete=models.CASCADE, related_name='connections', blank=False)
    start_fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE, related_name='start_muff_connections',
                                    blank=True, null=True)
    end_fiber = models.ForeignKey(Fiber, on_delete=models.CASCADE, related_name='end_muff_connections',
                                  blank=True, null=True)

    def get_start(self):
        return self.start_fiber

    def get_end(self):
        return self.end_fiber

    class Meta:
        verbose_name = 'Волоконная сварка'
        verbose_name_plural = 'Волоконные сварки'

    def __str__(self):
        return f'Сварка №{self.id}'
