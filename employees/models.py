from django.db import models
from fops.models import Fops

class Employee(models.Model):
    TAX_PRIVILEGE_CHOICES = [
        ('none', 'Без пільги'),
        ('100', '100% НСП (базова)'),
        ('150', '150% НСП (одинова мати / діти-інваліди)'),
        ('200', '200% НСП')
    ]

    WORK_SCHEDULE_CHOICES = [
        ('full_40', "П'ятиденка (40год/тиж, 8 год/день"),
        ('part_20', 'Неповний робочий день (20 год/тиж, 4 год/день)'),
        ('part_10', 'Неповний робочий день (10 год/тиж, 2 год/день)'),
        ('shift', 'Змінний графік'),
    ]

    fop = models.ForeignKey(
        Fops,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='ФОП Роботодавець'
    )
    full_name = models.CharField(
        'ПІБ працівника',
        max_length=150,
        help_text="Наприклад: Іванов Іван Іванович"
    )
    tax_id = models.CharField(
        'РНОКПП (ІПН)',
        max_length=10,
        help_text="Наприклад: 3126501237"
    )
    birth_date = models.DateField(
        'Дата народження',
    )
    position = models.CharField(
        'Посада',
        max_length=150,
        help_text="Згідно з класифікатором професій"
    )
    hire_date = models.DateField(
        'Дата прийняття на роботу'
    )
    salary = models.DecimalField(
        'Оклад (грн)',
        max_digits=10,
        decimal_places=2,
    )
    is_primary = models.BooleanField(
        'Основне місце роботи',
        default=True,
        help_text='Якщо Ні — сумісництво (неосновне)'
    )
    tax_privilege = models.CharField(
        'Пільга з ПДФО',
        max_length=10,
        choices=TAX_PRIVILEGE_CHOICES,
        default='none',
    )
    work_schedule = models.CharField(
        'Графік роботи',
        max_length=20,
        choices=WORK_SCHEDULE_CHOICES,
        default='full_40'
    )
    is_active = models.BooleanField(
        'Працює',
        default=True,
    )
    created_at = models.DateTimeField(
        'Створено в системі',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.position}) - ФОП {self.fop.full_name}"
