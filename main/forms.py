from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={"class": "form-control mr-2",
                                                                                     "placeholder": "Поиск",
                                                                                     "aria-label": "Search"}))


class SortForm(forms.Form):
    sorting = forms.CharField(required=False, label='', widget=forms.Select(choices=[("-id", "Дате добавления"),
                                                                                     ("last_name", "Фамилии")],
                                                                            attrs={"class": "form-select",
                                                                                   'onchange': 'this.form.submit();'}))
