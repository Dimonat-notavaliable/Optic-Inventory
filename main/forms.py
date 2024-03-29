from django import forms
from django.core.exceptions import ValidationError

from .models import Facility, Hardware, Cable, Muff, FOCL, MuffConnection, FacilityConnection, Cross, AdapterType


class DynamicModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        try:
            value = super().to_python(value)
        except ValidationError:
            key = self.to_field_name or 'pk'
            muff = Muff.objects.filter(**{key: value})
            facility = Facility.objects.filter(**{key: value})
            if facility.exists():
                value = facility
            elif muff.exists():
                value = muff
            else:
                raise
            value = value.first()
        return value


class SearchForm(forms.Form):
    search = forms.CharField(required=False, label='',
                             widget=forms.TextInput(attrs={"class": "form-control shadow-none border-0 mr-2",
                                                           "placeholder": "Поиск",
                                                           "aria-label": "Search"}))


class UsersSortForm(forms.Form):
    sorting = forms.CharField(required=False, label='', widget=forms.Select(choices=[("-id", "Дате добавления"),
                                                                                     ("last_name", "Фамилии")],
                                                                            attrs={"class": "form-select w-auto",
                                                                                   'onchange': 'this.form.submit()'}))


class HardwareSortForm(forms.Form):
    sorting = forms.CharField(required=False, label='', widget=forms.Select(choices=[("-id", "Дате добавления"),
                                                                                     ("marking", "Наименованию")],
                                                                            attrs={"class": "form-select w-auto",
                                                                                   "data-width": "auto",
                                                                                   "onchange": "this.form.submit()"}))


class CentersSortForm(forms.Form):
    sorting = forms.CharField(required=False, label='', widget=forms.Select(choices=[("-id", "Дате добавления"),
                                                                                     ("name", "Наименованию")],
                                                                            attrs={"class": "form-select w-auto",
                                                                                   "data-width": "auto",
                                                                                   "onchange": "this.form.submit()"}))


class FacilityForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Наименование',
                           widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                         "data-width": "auto"}))
    floor_count = forms.IntegerField(required=True, label='Количество этажей',
                                     widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                   "data-width": "auto"}))
    latitude = forms.DecimalField(required=True, label='Широта',
                                  widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                "data-width": "auto"}))
    longitude = forms.DecimalField(required=True, label='Долгота',
                                   widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                 "data-width": "auto"}))

    class Meta:
        model = Facility
        fields = ["name", "floor_count", "latitude", "longitude"]


class MuffForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Наименование',
                           widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                         "data-width": "auto"}))
    capacity = forms.IntegerField(required=True, label='Вместимость',
                                  widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                "data-width": "auto"}))
    latitude = forms.DecimalField(required=True, label='Широта',
                                  widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                "data-width": "auto"}))
    longitude = forms.DecimalField(required=True, label='Долгота',
                                   widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                 "data-width": "auto"}))

    class Meta:
        model = Muff
        fields = ["name", "capacity", "latitude", "longitude"]


class HardwareForm(forms.ModelForm):
    facility = forms.ModelChoiceField(required=True, label='Сооружение связи',
                                      queryset=Facility.objects.all().order_by('name'),
                                      widget=forms.Select(attrs={"class": "form-select w-auto",
                                                                 "data-width": "auto"}),
                                      empty_label="-- Выберите значение --"
                                      )
    marking = forms.CharField(required=True, label='Наименование',
                              widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                            "data-width": "auto"}))
    type = forms.CharField(required=True, label='Тип',
                           widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                         "data-width": "auto"}))
    port_count = forms.IntegerField(required=True, label='Количество портов',
                                    widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                  "data-width": "auto"}))
    IP = forms.GenericIPAddressField(required=False, label='IP-адрес',
                                     widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                   "data-width": "auto"}))
    MAC = forms.CharField(required=False, label='MAC-адрес',
                          widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                        "data-width": "auto"}))

    class Meta:
        model = Hardware
        fields = ["facility", "marking", "type", "port_count", "IP", "MAC"]


class FOCLForm(forms.ModelForm):
    start_type = forms.ChoiceField(required=True, label='Тип начального узла связи', choices=[],
                                   widget=forms.Select(attrs={"class": "form-select w-auto",
                                                              "data-width": "auto"}))

    start = DynamicModelChoiceField(required=True, label='Начальный узел связи',
                                    queryset=Facility.objects.all(),
                                    widget=forms.Select(attrs={"class": "form-select w-auto",
                                                               "data-width": "auto"}),
                                    empty_label="— Выберите тип —")

    end_type = forms.ChoiceField(required=True, label='Тип конечного узла связи', choices=[],
                                 widget=forms.Select(attrs={"class": "form-select w-auto",
                                                            "data-width": "auto"}))

    end = DynamicModelChoiceField(required=True, label='Конечный узел связи',
                                  queryset=Facility.objects.all(),
                                  widget=forms.Select(attrs={"class": "form-select w-auto",
                                                             "data-width": "auto"}),
                                  empty_label="— Выберите тип —")

    cable = forms.ModelChoiceField(required=True, label='Кабель',
                                   queryset=Cable.objects.all().order_by('producer'),
                                   widget=forms.Select(attrs={"class": "form-select w-auto",
                                                              "data-width": "auto"}),
                                   empty_label="— Выберите значение —")
    cable_length = forms.DecimalField(required=True, label='Длина по кабелю (м.)',
                                      widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                    "data-width": "auto"}))
    fiber_length = forms.DecimalField(required=False, label='Длина по волокну (м.)',
                                      widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                    "data-width": "auto"}))

    class Meta:
        model = FOCL
        fields = ["start_type", "start", "end_type", "end", "cable", "cable_length", "fiber_length"]

    def __init__(self, *args, **kwargs):
        super(FOCLForm, self).__init__(*args, **kwargs)

        CENTER_CHOICES = [
            (None, "— Выберите значение —"),
            ("facility", "Сооружение связи"),
            ("muff", "Муфта"),
        ]

        self.fields['start_type'].choices = CENTER_CHOICES
        self.fields['end_type'].choices = CENTER_CHOICES
        self.fields['start'].queryset = Facility.objects.none()
        self.fields['end'].queryset = Facility.objects.none()

    def save(self, commit=True):
        instance = super(FOCLForm, self).save(commit=False)
        instance.cable_length = self.cleaned_data.get('cable_length')
        instance.cable = self.cleaned_data.get('cable')
        instance.fiber_length = self.cleaned_data.get('fiber_length')

        instance.save()

        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')

        if self.cleaned_data.get('start_type') == 'muff':
            start_connection = MuffConnection(focl=instance, muff=start, is_start=True)
            start_connection.save()
        elif self.cleaned_data.get('start_type') == 'facility':
            start_connection = FacilityConnection(focl=instance, facility=start, is_start=True)
            start_connection.save()

        if self.cleaned_data.get('end_type') == 'muff':
            end_connection = MuffConnection(focl=instance, muff=end, is_start=False)
            end_connection.save()
        elif self.cleaned_data.get('end_type') == 'facility':
            end_connection = FacilityConnection(focl=instance, facility=end, is_start=False)
            end_connection.save()

        return instance


class CrossForm(forms.ModelForm):
    facility = forms.ModelChoiceField(required=True, label='Сооружение связи',
                                      queryset=Facility.objects.all().order_by('name'),
                                      widget=forms.Select(attrs={"class": "form-select w-auto",
                                                                 "data-width": "auto"}),
                                      empty_label="-- Выберите значение --")
    adapter_count = forms.IntegerField(required=True, label='Количество адаптеров',
                                       widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                     "data-width": "auto"}))
    linear_type = forms.ModelChoiceField(required=True, label='Тип адаптеров линейной стороны',
                                         queryset=AdapterType.objects.all().order_by('marking'),
                                         widget=forms.Select(attrs={"class": "form-select w-auto",
                                                                    "data-width": "auto"}))
    station_type = forms.ModelChoiceField(required=True, label='Тип адаптеров линейной стороны',
                                          queryset=AdapterType.objects.all().order_by('marking'),
                                          widget=forms.Select(attrs={"class": "form-select w-auto",
                                                                     "data-width": "auto"}))

    class Meta:
        model = Cross
        fields = ["facility", "adapter_count", "linear_type", "station_type"]


class UserRightsForm(forms.ModelForm):
    is_active = forms.BooleanField(required=False, label='Активен',
                                   widget=forms.CheckboxInput(attrs={"class": "form-check-input shadow-none"}),
                                   )
    is_writer = forms.BooleanField(required=False, label='Редактор',
                                   widget=forms.CheckboxInput(attrs={"class": "form-check-input shadow-none"}))
    is_superuser = forms.BooleanField(required=False, label='Администратор',
                                      widget=forms.CheckboxInput(attrs={"class": "form-check-input shadow-none"}))

    class Meta:
        model = Hardware
        fields = ["is_active", "is_writer", "is_superuser"]
