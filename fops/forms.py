from django import forms
from .models import Fops


class FopsForm(forms.ModelForm):
    class Meta:
        model = Fops
        fields = '__all__'  # Виводимо абсолютно всі поля моделі Fops
        labels = {
            'full_name': 'Повна назва / ПІБ ФОП',
            'tax_id': 'Податковий номер (ІПН / ЄДРПОУ)',
            'opf_code': 'Код ОПФГ',
            'postal_code': 'Поштовий індекс',
            'region': 'Область',
            'district': 'Район',
            'city': 'Населений пункт',
            'katottg': 'Код КАТОТТГ',
            'street': 'Вулиця',
            'building': 'Будинок / Квартира',
            'main_kved': 'Основний КВЕД',
            'additional_kveds': 'Додаткові КВЕДи',
            'tax_system': 'Система оподаткування',
            'dps_code': 'Код ДПС',
            'dps_name': 'Назва органу ДПС',
            'pfu_code': 'Код органу ПФУ',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'наприклад, ФОП Петренко Петро Петрович'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-значний ІПН або 8-значний ЄДРПОУ'}),
            'opf_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '910'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01001'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Київська обл.'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Обухівський р-н'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'м. Київ'}),
            'katottg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UA80000000000093317'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'вул. Хрещатик'}),
            'building': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'буд. 1, кв. 10'}),
            'main_kved': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "62.01 Комп'ютерне програмування"}),
            'additional_kveds': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '62.02, 62.09, 63.11'}),
            'tax_system': forms.Select(attrs={'class': 'form-select'}),
            'dps_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2655'}),
            'dps_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ГУ ДПС у м. Києві'}),
            'pfu_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '26001'}),
        }

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get('tax_id', '').strip()
        if not tax_id.isdigit():
            raise forms.ValidationError('Податковий номер повинен містити лише цифри.')
        if len(tax_id) not in (8, 10):
            raise forms.ValidationError('Податковий номер повинен містити 8 або 10 цифр.')
        return tax_id