from django import forms


class MaterialXMLForm(forms.Form):
    xml = forms.FileField()
