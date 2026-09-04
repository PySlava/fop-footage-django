from django.db import models
from employees.models import Employee


class HiringOrder(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='hiring_order')
    order_number = models.CharField(
        'Номер заказу',
        max_length=20
    )
    order_date = models.DateField(
        'Дата наказу'
    )
    pdf_file = models.FileField(
        'PDF-file',
        upload_to='orders/pdf/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Наказ про прийняття'
        verbose_name_plural = 'Накази про прийняття'

    def __str__(self):
        return f"Наказ № {self.order_number} від {self.order_date} ({self.employee.full_name})"