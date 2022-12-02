from django import forms
from django.core.validators import FileExtensionValidator


class MaterialXMLForm(forms.Form):
    # This is the form we use to upload xml file
    xml = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['xml'],
                                                             message='El archivo debe ser xml')
                                      ])

    # xml = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
