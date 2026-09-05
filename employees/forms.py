from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'fop',
            'full_name',
            'tax_id',
            'birth_date',
            'position',
            'hire_date',
            'salary',
            'employment_type',
        ]
        labels = {
            'fop': 'ФОП Роботодавець',
            'full_name': 'ПІБ Працівника (повністю)',
            'tax_id': 'Податковий номер (ІПН)',
            'birth_date': 'Дата народження',
            'position': 'Посада',
            'hire_date': 'Дата прийняття на роботу',
            'salary': 'Оклад / Ставка (грн)',
            'employment_type': 'Тип зайнятості',
        }
        widgets = {
            'fop': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Шевченко Тарас Григорович'
            }),
            'tax_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-значний ІПН (наприклад, 1234567890)'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Бухгалтер, Менеджер, Розробник...'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '20000.00',
                'step': '0.01'
            }),
            'employment_type': forms.Select(
                choices=[
                    ('main', 'Основне місце роботи'),
                    ('part_time', 'Сумісництво'),
                ],
                attrs={'class': 'form-select'}
            ),
        }