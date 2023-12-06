from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={"class": "form-control border-0 mr-2",
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