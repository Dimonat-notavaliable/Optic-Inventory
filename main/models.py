from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Кабель
class Cable(models.Model):
    producer = models.CharField()
    marking = models.CharField()

    class Meta:
        verbose_name = 'Кабель'
        verbose_name_plural = 'Кабели'


# Модуль в кабеле
class Module(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    color = models.CharField(_("Цвет"), blank=False, default="Белый")
    color_HEX = models.CharField(_("Цвет HEX"), blank=False, default="#ffffff")
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE,  related_name='module', blank=False)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


# Волокно в модуле
class Fiber(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    color = models.CharField(_("Цвет"), blank=False, default="Белый")
    color_HEX = models.CharField(_("Цвет HEX"), blank=False, default="#ffffff")
    start_fiber = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='end',
                                    blank=True, null=True)
    end_fiber = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='start',
                                  blank=True, null=True)

    class Meta:
        verbose_name = 'Волокно'
        verbose_name_plural = 'Волокна'


# Волоконно-оптическая линия связи
class FOCL(models.Model):
    cable_length = models.IntegerField(_("Длина по кабелю"), blank=False,
                                       validators=[MinValueValidator(0)])
    fiber_length = models.IntegerField(_("Длина по волокну"), blank=True, null=True,
                                       validators=[MinValueValidator(0)])
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, related_name='FOCL', blank=False)

    class Meta:
        verbose_name = 'Волоконно-оптическая линия связи'
        verbose_name_plural = 'Волоконно-оптические линии связи'


# Промежуточные координаты линии связи
class FOCLInterCoordinates(models.Model):
    latitude = models.DecimalField(_("Широта"), max_digits=9, decimal_places=6, blank=False)
    longitude = models.DecimalField(_("Долгота"), max_digits=9, decimal_places=6, blank=False)
    focl = models.ForeignKey(FOCL, on_delete=models.CASCADE, related_name='inter_coordinates', blank=False)

    class Meta:
        verbose_name = 'Промежуточная точка ВОЛС'
        verbose_name_plural = 'Промежуточные точки ВОЛС'


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


# Сетевое оборудование (маршрутизаторы, IP-телефоны, коммутаторы и т.д.)
class Hardware(models.Model):
    marking = models.CharField(_("Название"), blank=False)
    type = models.CharField(_("Тип"), blank=False)
    floor = models.IntegerField(_("Этаж расположения"), blank=False, default=1,
                                validators=[MinValueValidator(1)])
    IP = models.IPAddressField(_("IP-адрес"), protocol="both", blank=True, null=True)
    MAC = models.CharField(_("MAC-адрес"), blank=True, null=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, related_name='hardware', blank=True, null=True)

    class Meta:
        verbose_name = 'Сетевое оборудование'
        verbose_name_plural = 'Сетевое оборудование'


# Порт сетевого оборудования
class Port(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name='ports', blank=False)
    port = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='port', blank=True, null=True)

    class Meta:
        verbose_name = 'Порт оборудования'
        verbose_name_plural = 'Порты оборудования'


# Оптический кросс
class Cross(models.Model):
    floor = models.IntegerField(_("Этаж расположения"), blank=False, default=1,
                                validators=[MinValueValidator(1)])
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='crosses', blank=False)

    class Meta:
        verbose_name = 'Оптический кросс'
        verbose_name_plural = 'Оптические кроссы'


# Адаптер оптического кросса
class Adapter(models.Model):
    number = models.IntegerField(_("Номер"), blank=False, validators=[MinValueValidator(1)])
    type = models.CharField(_("Тип"), blank=False)
    is_linear = models.BooleanField(_("Линейная сторона"), blank=False)
    cross = models.ForeignKey(Cross, on_delete=models.CASCADE, related_name='adapters', blank=False)

    class Meta:
        verbose_name = 'Адаптер кросса'
        verbose_name_plural = 'Адаптеры кроссов'
