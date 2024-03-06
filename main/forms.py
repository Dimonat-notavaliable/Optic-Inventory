from django import forms

from .models import Facility


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
    name = forms.CharField(required=True, label='Наименование', widget=forms.TextInput(attrs={"class": "form-control w-auto",
                                                                                  "data-width": "auto"}))
    floor_count = forms.IntegerField(required=True, label='Кол-во этажей',
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
