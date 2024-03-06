from django import forms

from .models import Facility, Hardware


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


class FacilitiesSortForm(forms.Form):
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
