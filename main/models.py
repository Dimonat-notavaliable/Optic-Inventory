from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

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


# Муфта
class Muff(CommunicationCenter):
    capacity = models.IntegerField(_("Вместимость"), blank=False, default=64,
                                   validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Муфта'
        verbose_name_plural = 'Муфты'


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

    def __str__(self):
        return f'{self.marking} #{self.id}'


# Порт сетевого оборудования
class Port(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name='ports', blank=False)
    port = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='commutation', blank=True, null=True)

    class Meta:
        verbose_name = 'Порт оборудования'
        verbose_name_plural = 'Порты оборудования'

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

    def __str__(self):
        type = "линейный" if self.is_linear else "станционный"
        return f'{self.cross}: Адаптер {self.number} {type}'


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
            count += len(module.fibers.all())
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


class FOCL(models.Model):
    cable = models.OneToOneField(Cable, on_delete=models.CASCADE, related_name='focl', blank=False)
    cable_length = models.DecimalField(_("Длина по кабелю"), max_digits=9, decimal_places=2, blank=False)
    fiber_length = models.DecimalField(_("Длина по волокну"), max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Линия связи'
        verbose_name_plural = 'Линии связи'

    def __str__(self):
        return f'Линия связи: {self.cable}'

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


class MuffConnection(models.Model):
    focl = models.ForeignKey(FOCL, on_delete=models.CASCADE, related_name='connection_muff', blank=False)
    muff = models.ForeignKey(Muff, on_delete=models.CASCADE, related_name='connection', blank=False)
    is_start = models.BooleanField(_("Начало"), blank=False)

    class Meta:
        verbose_name = 'Следование через муфту'
        verbose_name_plural = 'Следования через муфту'

    def __str__(self):
        return f'{self.focl} через {self.muff}'


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
