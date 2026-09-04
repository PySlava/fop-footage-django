from django.db import models
from employees.models import Employee


class DpsNotification(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Чернетка'),
        ('sent', 'Відправлено'),
        ('accepted', 'Прийнято (Квитанція №2)'),
    )

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='dps_notification'
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    xml_file = models.FileField(
        'XML file',
        upload_to='dps/xml/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Повідомлення ДПС'
        verbose_name_plural = 'Повідомлення ДПС'

    def __str__(self):
        return f"Повідомлення ДПС - {self.employee.full_name} ({self.get_status_display})"