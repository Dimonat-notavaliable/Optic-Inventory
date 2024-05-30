from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import Muff, FOCL


# Схема муфты
class MuffScheme(models.Model):
    muff = models.ForeignKey(Muff, on_delete=models.CASCADE, related_name='schemes', blank=False)
    last_change = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Схема муфты'
        verbose_name_plural = 'Схемы муфты'

    def __str__(self):
        return f'Схема муфты {self.muff.id} от {self.last_change}'


# Линия связи на схеме муфты
class MuffSchemeFOCL(models.Model):
    DIRECTION_CHOICES = (
        ("up", "UP"),
        ("down", "DOWN"),
        ("left", "LEFT"),
        ("right", "RIGHT"),
    )

    scheme = models.ForeignKey(MuffScheme, on_delete=models.CASCADE, related_name='focls', blank=False)
    focl = models.ForeignKey(FOCL, on_delete=models.CASCADE, related_name='scheme_muff', blank=False)
    coordinate_x = models.IntegerField(_("Координата x"), default=100, blank=False)
    coordinate_y = models.IntegerField(_("Координата y"), default=100, blank=False)
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES, default="right")

    class Meta:
        verbose_name = 'Линия связи на схеме муфты'
        verbose_name_plural = 'Линии связи на схеме муфты'

    def __str__(self):
        return f'Линия #{self.focl.id} на {self.scheme}'
