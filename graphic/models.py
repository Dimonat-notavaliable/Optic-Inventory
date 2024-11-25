from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import FOCL, Facility, Muff


# Схема муфты
class MuffScheme(models.Model):
    muff = models.ForeignKey(
        Muff, on_delete=models.CASCADE, related_name="schemes", blank=False
    )
    last_change = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Схема муфты"
        verbose_name_plural = "Схемы муфты"

    def __str__(self):
        return f"Схема муфты {self.muff.id} от {self.last_change}"


# Линия связи на схеме муфты
class MuffSchemeFOCL(models.Model):
    DIRECTION_CHOICES = (
        ("up", "UP"),
        ("down", "DOWN"),
        ("left", "LEFT"),
        ("right", "RIGHT"),
    )

    scheme = models.ForeignKey(
        MuffScheme, on_delete=models.CASCADE, related_name="focls", blank=False
    )
    focl = models.ForeignKey(
        FOCL, on_delete=models.CASCADE, related_name="scheme_muff", blank=False
    )
    coordinate_x = models.IntegerField(_("Координата x"), default=100, blank=False)
    coordinate_y = models.IntegerField(_("Координата y"), default=100, blank=False)
    direction = models.CharField(
        max_length=5, choices=DIRECTION_CHOICES, default="right"
    )

    class Meta:
        verbose_name = "Линия связи на схеме муфты"
        verbose_name_plural = "Линии связи на схеме муфты"

    def __str__(self):
        return f"Линия #{self.focl.id} на {self.scheme}"


# Схема сооружения связи
class FacilityScheme(models.Model):
    facility = models.ForeignKey(
        Facility, on_delete=models.CASCADE, related_name="schemes", blank=False
    )
    last_change = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Схема сооружения связи"
        verbose_name_plural = "Схемы сооружения связи"

    def __str__(self):
        return f"Схема сооружения связи {self.facility.id} от {self.last_change}"


# Тип объекта на схеме сооружения связи
class SchemeObjectType(models.Model):
    marking = models.CharField(_("Наименование"), blank=False, unique=True)

    class Meta:
        verbose_name = "Тип объекта на схема"
        verbose_name_plural = "Типы объектов на схеме"

    def __str__(self):
        return f"Тип: {self.marking}"


# Объект на схеме сооружения связи
class FacilitySchemeObject(models.Model):
    DIRECTION_CHOICES = (
        ("up", "UP"),
        ("down", "DOWN"),
        ("left", "LEFT"),
        ("right", "RIGHT"),
    )

    scheme = models.ForeignKey(
        FacilityScheme, on_delete=models.CASCADE, related_name="drawings", blank=False
    )
    object_id = models.IntegerField(_("Идентификатор объекта"), blank=False)
    object_type = models.ForeignKey(
        SchemeObjectType, on_delete=models.CASCADE, related_name="drawings", blank=False
    )
    coordinate_x = models.IntegerField(_("Координата x"), default=100, blank=False)
    coordinate_y = models.IntegerField(_("Координата y"), default=100, blank=False)
    direction = models.CharField(
        max_length=5, choices=DIRECTION_CHOICES, default="right"
    )

    class Meta:
        verbose_name = "Объект на схеме сооружения связи"
        verbose_name_plural = "Объекты на схеме сооружения связи"

    def __str__(self):
        return f"{self.object_type.marking} #{self.object_id} на {self.scheme}"
