from django import forms

class Calculate(forms.Form):
    support_value= forms.IntegerField()
    confident_value = forms.IntegerField()
    lift_value = forms.IntegerField()


class UploadFileForm(forms.Form):
    file = forms.FileField()
