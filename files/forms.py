from django import forms


class ImportForm(forms.Form):
    file = forms.FileField(
        required=True,
        label="Файл формата .xslx или .csv",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
