from django import forms
from django.core.exceptions import ValidationError

from .models import (
    FOCL,
    Adapter,
    AdapterType,
    Cable,
    Connection,
    Cross,
    Facility,
    FacilityConnection,
    Fiber,
    Hardware,
    HardwareType,
    Module,
    Muff,
    MuffConnection,
    Port,
)

COLOR_PALETTE = {
    "#FFFFFF": "Белый",
    "#000000": "Черный",
    "#00FFFF": "Бирюзовый",
    "#0000FF": "Синий",
    "#FF00FF": "Розовый",
    "#808080": "Серый",
    "#008000": "Зеленый",
    "#00FF00": "Свтл. Зеленый",
    "#800000": "Тмн. Красный",
    "#000080": "Тмн. Синий",
    "#808000": "Оливковый",
    "#800080": "Фиолетовый",
    "#FF0000": "Красный",
    "#C0C0C0": "Серебряный",
    "#008080": "Серо-зеленый",
    "#FFFF00": "Желтый",
}


class DynamicModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        try:
            value = super().to_python(value)
        except ValidationError:
            return int(value)
        return value


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control shadow-none border-0 mr-2",
                "placeholder": "Поиск",
                "aria-label": "Search",
            }
        ),
    )


class UsersSortForm(forms.Form):
    sorting = forms.CharField(
        required=False,
        label="",
        widget=forms.Select(
            choices=[("-id", "Дате добавления"), ("last_name", "Фамилии")],
            attrs={"class": "form-select w-auto", "onchange": "this.form.submit()"},
        ),
    )


class HardwareSortForm(forms.Form):
    sorting = forms.CharField(
        required=False,
        label="",
        widget=forms.Select(
            choices=[("-id", "Дате добавления"), ("marking", "Наименованию")],
            attrs={
                "class": "form-select w-auto",
                "data-width": "auto",
                "onchange": "this.form.submit()",
            },
        ),
    )


class CentersSortForm(forms.Form):
    sorting = forms.CharField(
        required=False,
        label="",
        widget=forms.Select(
            choices=[("-id", "Дате добавления"), ("name", "Наименованию")],
            attrs={
                "class": "form-select w-auto",
                "data-width": "auto",
                "onchange": "this.form.submit()",
            },
        ),
    )


class FOCLsSortForm(forms.Form):
    sorting = forms.CharField(
        required=False,
        label="",
        widget=forms.Select(
            choices=[("-id", "Дате добавления"), ("cable_length", "Протяженности")],
            attrs={
                "class": "form-select w-auto",
                "data-width": "auto",
                "onchange": "this.form.submit()",
            },
        ),
    )


class CrossesSortForm(forms.Form):
    sorting = forms.CharField(
        required=False,
        label="",
        widget=forms.Select(
            choices=[("-id", "Дате добавления"), ("adapter_count", "Числу адаптеров")],
            attrs={
                "class": "form-select w-auto",
                "data-width": "auto",
                "onchange": "this.form.submit()",
            },
        ),
    )


class FacilityForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="Наименование",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    floor_count = forms.IntegerField(
        required=True,
        label="Количество этажей",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    latitude = forms.DecimalField(
        required=True,
        label="Широта",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    longitude = forms.DecimalField(
        required=True,
        label="Долгота",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )

    class Meta:
        model = Facility
        fields = ["name", "floor_count", "latitude", "longitude"]


class MuffForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="Наименование",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    capacity = forms.IntegerField(
        required=True,
        label="Вместимость",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    latitude = forms.DecimalField(
        required=True,
        label="Широта",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    longitude = forms.DecimalField(
        required=True,
        label="Долгота",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )

    class Meta:
        model = Muff
        fields = ["name", "capacity", "latitude", "longitude"]


class HardwareForm(forms.ModelForm):
    marking = forms.CharField(
        required=True,
        label="Наименование",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    facility = forms.ModelChoiceField(
        required=True,
        label="Сооружение связи",
        queryset=Facility.objects.all().order_by("name"),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="-- Выберите значение --",
    )
    floor = forms.IntegerField(
        required=True,
        label="Этаж расположения",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    type = forms.ModelChoiceField(
        required=True,
        label="Тип оборудования",
        queryset=HardwareType.objects.all().order_by("marking"),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
    )
    port_count = forms.IntegerField(
        required=True,
        label="Количество портов",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    IP = forms.GenericIPAddressField(
        required=False,
        label="IP-адрес",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    MAC = forms.CharField(
        required=False,
        label="MAC-адрес",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )

    class Meta:
        model = Hardware
        fields = ["facility", "floor", "marking", "type", "port_count", "IP", "MAC"]


class HardwareCommutationForm(forms.ModelForm):
    commutation_type = forms.ChoiceField(
        required=True,
        label="Тип соединения",
        choices=[],
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
    )
    commutation = DynamicModelChoiceField(
        required=True,
        label="Соединение",
        queryset=Port.objects.none(),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="— Выберите тип —",
    )

    class Meta:
        model = Connection
        fields = ["commutation_type", "commutation"]

    def __init__(self, *args, **kwargs):
        super(HardwareCommutationForm, self).__init__(*args, **kwargs)

        self.fields["commutation_type"].choices = [
            (None, "— Выберите значение —"),
            ("adapter", "Адаптер кросса"),
            ("port", "Порт оборудования"),
        ]

    def save(self, commit=False):
        instance = super(HardwareCommutationForm, self).save(commit=False)

        commutation = self.cleaned_data.get("commutation")

        if self.cleaned_data.get("commutation_type") == "adapter":
            adapter = Adapter.objects.get(pk=commutation)
            instance.facility = adapter.cross.facility
            instance.start_adapter = adapter

        elif self.cleaned_data.get("commutation_type") == "port":
            port = Port.objects.get(pk=commutation)
            instance.facility = port.hardware.facility
            instance.start_port = port

        return instance


class FOCLForm(forms.ModelForm):
    start_type = forms.ChoiceField(
        required=True,
        label="Тип начального узла связи",
        choices=[],
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
    )

    start = DynamicModelChoiceField(
        required=True,
        label="Начальный узел связи",
        queryset=Facility.objects.none(),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="— Выберите тип —",
    )

    end_type = forms.ChoiceField(
        required=True,
        label="Тип конечного узла связи",
        choices=[],
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
    )

    end = DynamicModelChoiceField(
        required=True,
        label="Конечный узел связи",
        queryset=Facility.objects.none(),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="— Выберите тип —",
    )

    cable = forms.ModelChoiceField(
        required=True,
        label="Кабель",
        queryset=Cable.objects.filter(focl=None).order_by("producer"),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="— Выберите значение —",
    )
    cable_length = forms.DecimalField(
        required=True,
        label="Длина по кабелю (м.)",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    fiber_length = forms.DecimalField(
        required=False,
        label="Длина по волокну (м.)",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )

    class Meta:
        model = FOCL
        fields = [
            "start_type",
            "start",
            "end_type",
            "end",
            "cable",
            "cable_length",
            "fiber_length",
        ]

    def __init__(self, *args, **kwargs):
        super(FOCLForm, self).__init__(*args, **kwargs)

        CENTER_CHOICES = [
            (None, "— Выберите значение —"),
            ("facility", "Сооружение связи"),
            ("muff", "Муфта"),
        ]

        self.fields["start_type"].choices = CENTER_CHOICES
        self.fields["end_type"].choices = CENTER_CHOICES

    def save(self, commit=True):
        instance = super(FOCLForm, self).save(commit=False)
        instance.cable_length = self.cleaned_data.get("cable_length")
        instance.cable = self.cleaned_data.get("cable")
        instance.fiber_length = self.cleaned_data.get("fiber_length")

        instance.save()

        start = self.cleaned_data.get("start")
        end = self.cleaned_data.get("end")

        for connection_type, connection in [("start_type", start), ("end_type", end)]:
            is_start = connection_type == "start_type"

            if self.cleaned_data.get(connection_type) == "muff":
                muff = Muff.objects.get(pk=connection)
                connection = MuffConnection(focl=instance, muff=muff, is_start=is_start)
                connection.save()

            elif self.cleaned_data.get(connection_type) == "facility":
                facility = Facility.objects.get(pk=connection)
                connection = FacilityConnection(
                    focl=instance, facility=facility, is_start=is_start
                )
                connection.save()

        return instance


class CrossForm(forms.ModelForm):
    facility = forms.ModelChoiceField(
        required=True,
        label="Сооружение связи",
        queryset=Facility.objects.all().order_by("name"),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="-- Выберите значение --",
    )
    adapter_count = forms.IntegerField(
        required=True,
        label="Количество адаптеров",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    linear_type = forms.ModelChoiceField(
        required=True,
        label="Тип адаптеров линейной стороны",
        queryset=AdapterType.objects.all().order_by("marking"),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
    )
    station_type = forms.ModelChoiceField(
        required=True,
        label="Тип адаптеров станционной стороны",
        queryset=AdapterType.objects.all().order_by("marking"),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
    )

    class Meta:
        model = Cross
        fields = ["facility", "adapter_count", "linear_type", "station_type"]


class LinearAdapterCommutationForm(forms.ModelForm):
    commutation = forms.ModelChoiceField(
        required=True,
        label="Соединение",
        queryset=Fiber.objects.none(),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="-- Выберите волокно --",
    )

    class Meta:
        model = Connection
        fields = ["commutation"]

    def __init__(self, cross, *args, **kwargs):
        super(LinearAdapterCommutationForm, self).__init__(*args, **kwargs)
        facility = Cross.objects.get(pk=cross).facility
        connections = facility.connection
        cables = [connection.focl.cable for connection in connections.all()]
        free_fiber_ids = []
        for cable in cables:
            for module in cable.modules.all():
                free_fiber_ids += [
                    fiber.id
                    for fiber in module.fibers.all()
                    if not (
                        fiber.is_facility_commutated() or fiber.is_muff_commutated()
                    )
                ]

        self.fields["commutation"].queryset = Fiber.objects.filter(
            id__in=free_fiber_ids
        )

    def save(self, commit=False):
        instance = super(LinearAdapterCommutationForm, self).save(commit=False)

        fiber = self.cleaned_data.get("commutation")
        instance.start_fiber = fiber

        return instance


class StationAdapterCommutationForm(forms.ModelForm):
    commutation = forms.ModelChoiceField(
        required=True,
        label="Соединение",
        queryset=Fiber.objects.none(),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="-- Выберите оборудование --",
    )

    class Meta:
        model = Connection
        fields = ["commutation"]

    def __init__(self, cross, *args, **kwargs):
        super(StationAdapterCommutationForm, self).__init__(*args, **kwargs)
        facility = Cross.objects.get(pk=cross).facility
        hardware = facility.hardware.all()
        free_port_ids = []
        for one in hardware:
            free_port_ids += [
                port.id for port in one.ports.all() if not port.is_commutated()
            ]
        self.fields["commutation"].queryset = Port.objects.filter(id__in=free_port_ids)

    def save(self, commit=False):
        instance = super(StationAdapterCommutationForm, self).save(commit=False)

        port = self.cleaned_data.get("commutation")
        instance.end_port = port

        return instance


class UserRightsForm(forms.ModelForm):
    is_active = forms.BooleanField(
        required=False,
        label="Активен",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input shadow-none"}),
    )
    is_writer = forms.BooleanField(
        required=False,
        label="Редактор",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input shadow-none"}),
    )
    is_superuser = forms.BooleanField(
        required=False,
        label="Администратор",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input shadow-none"}),
    )

    class Meta:
        model = Hardware
        fields = ["is_active", "is_writer", "is_superuser"]


class FiberForm(forms.ModelForm):
    number = forms.IntegerField(
        required=True,
        label="Номер",
        widget=forms.TextInput(
            attrs={"class": "form-control w-auto", "data-width": "auto"}
        ),
    )
    module = forms.ModelChoiceField(
        required=True,
        label="Сооружение связи",
        queryset=Module.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select w-auto", "data-width": "auto"}
        ),
        empty_label="-- Выберите значение --",
    )

    hex = forms.CharField(
        required=True,
        label="Цвет",
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "swatchy-output swatchy-trigger swatchy-display",
            }
        ),
    )

    class Meta:
        model = Fiber
        fields = ["number", "module", "hex"]

    def save(self, commit=True):
        instance = super(FiberForm, self).save(commit=False)
        hex = self.cleaned_data.get("hex")
        instance.color = COLOR_PALETTE[hex]

        instance.save()

        return instance
