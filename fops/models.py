from django.db import models

class Fops(models.Model):
    TAX_SYSTEM_CHOICES = [
        ('group_1', 'Єдиний податок - 1 група'),
        ('group_2', 'Єдиний податок - 2 група'),
        ('group_3_5', 'Єдиний податок - 3 група (5%)'),
        ('group_3_pdv', 'Єдиний податок - 3 група (3% + ПДВ)'),
        ('general', 'Загальна система оподаткування'),
    ]

    full_name = models.CharField(
        'ПІБ ФОП',
        max_length=255,
        help_text="Наприклад: Іванов Іван Іванович"
    )
    tax_id = models.CharField(
        'РНОКПП (ІПН)',
        max_length=10,
        unique=True,
        help_text="Наприклад: 3126501237"
    )
    address = models.TextField(
        'Податкова адреса (по прописці)'
    )
    tax_system = models.CharField(
        'Система оподаткування',
        max_length=20,
        choices=TAX_SYSTEM_CHOICES,
        default='group_2',
        help_text="Наприклад: group_2"
    )
    iban = models.CharField(
        'Розрахунковий рахунок (IBAN)',
        max_length=35,
        blank=True,
        null=True,
        help_text="Наприклад: UA853996220000000260012335661"
    )
    kved = models.CharField(
        'Основний КВЕД',
        max_length=255,
        blank=True,
        null=True,
        help_text="Наприклад: 62.01 Комп'ютерне програмування"
    )
    created_at = models.DateTimeField(
        "Дата створення",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'ФОП'
        verbose_name_plural = 'ФОПи'
        ordering = ['full_name']

    def __str__(self):
        return f"ФОП {self.full_name} ({self.tax_id})"
