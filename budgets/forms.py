from django import forms


class MaterialXMLForm(forms.Form):
    # This is the form we use to upload xml file
    xml = forms.FileField()
