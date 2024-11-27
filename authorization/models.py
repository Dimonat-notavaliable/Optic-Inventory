from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    date_joined = None
    is_staff = None
    last_login = None
    groups = None
    user_permissions = None

    email = models.CharField(
        _("Email"),
        max_length=255,
        unique=True,
        help_text=_("Обязательное поле. 255 символов или меньше."),
        validators=[validate_email],
        error_messages={
            "unique": _("Пользователь с такой почтой уже существует."),
        },
    )
    password = models.CharField(max_length=255)
    last_name = models.CharField(_("Фамилия"), max_length=150, blank=False)
    first_name = models.CharField(_("Имя"), max_length=150, blank=False)
    patronymic = models.CharField(_("Отчество"), max_length=150, blank=True)
    is_active = models.BooleanField(
        _("Активен"),
        default=False,
        help_text=_(
            "Определяет, следует ли считать этого пользователя активным. "
            "Снимите этот флажок вместо удаления аккаунтов."
        ),
    )
    is_writer = models.BooleanField(_("Право редактирования"), default=False)
    is_superuser = models.BooleanField(verbose_name="Администратор", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    @property
    def get_full_name(self):
        if self.patronymic and self.last_name and self.first_name:
            return f"{self.last_name} {self.first_name[0]}. {self.patronymic[0]}."
        elif self.last_name and self.first_name:
            return f"{self.last_name} {self.first_name[0]}."
        else:
            return "Аноним"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
