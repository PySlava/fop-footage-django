from django import forms
from .models import Fops

class FopForm(forms.ModelForm):
    class Meta:
        model = Fops
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ПІБ підприємця'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tax_system': forms.Select(attrs={'class': 'form-select'}),
            'iban': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UA...'}),
            'kved': forms.TextInput(attrs={'class': 'form-control'}),
        }