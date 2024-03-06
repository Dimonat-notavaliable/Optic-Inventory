from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField


# Сооружение связи
class Facility(models.Model):
    name = models.CharField(_("Название"), blank=False)
    floor_count = models.IntegerField(_("Количество этажей"), blank=False, default=1,
                                      validators=[MinValueValidator(1)])
    latitude = models.DecimalField(_("Широта"), max_digits=9, decimal_places=6, blank=False)
    longitude = models.DecimalField(_("Долгота"), max_digits=9, decimal_places=6, blank=False)

    class Meta:
        verbose_name = 'Сооружение связи'
        verbose_name_plural = 'Сооружения связи'

    def __str__(self):
        return self.name


# Сетевое оборудование (маршрутизаторы, IP-телефоны, коммутаторы и т.д.)
class Hardware(models.Model):
    marking = models.CharField(_("Название"), blank=False)
    type = models.CharField(_("Тип"), blank=False)
    port_count = models.IntegerField(_("Количество портов"), default=0, blank=False)
    floor = models.IntegerField(_("Этаж расположения"), blank=False, default=1,
                                validators=[MinValueValidator(1)])
    IP = models.GenericIPAddressField(_("IP-адрес"), protocol="both", blank=True, null=True)
    MAC = models.CharField(_("MAC-адрес"), blank=True, null=True)
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
        port, _ = Port.objects.get_or_create(number=number+1, hardware=instance)


models.signals.post_save.connect(create_hardware_ports, sender=Hardware, dispatch_uid='create_hardware_ports')


class Cable(models.Model):
    producer = models.CharField(_("Производитель"), blank=False)
    marking = models.CharField(_("Маркировка"), blank=False)
    map_hex = ColorField(_("Цвет на карте"), default='#FFFFFF')

    class Meta:
        verbose_name = 'Кабель'
        verbose_name_plural = 'Кабели'

    def __str__(self):
        return f'{self.producer} {self.marking}'


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
