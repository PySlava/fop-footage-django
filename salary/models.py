from django.db import models


class SalaryCalculation(models.Model):
    timesheet = models.OneToOneField(
        'timesheet.Timesheet',
        on_delete=models.CASCADE,
        related_name='salary_calculation',
        verbose_name='Табель'
    )
    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Оклад'
    )
    norm_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Норма годин'
    )
    worked_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Відпрацьовано годин'
    )
    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Нараховано (Gross)'
    )
    pdfo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='ПДФО (18%)'
    )
    vz = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Військовий збір (5%)'
    )
    esv = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='ЄСВ (22%)'
    )
    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='До виплати (Net)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Розрахунок зарплати'
        verbose_name_plural = 'Розрахунки зарплати'

    def __str__(self):
        return f"Розрахунок ЗП: {self.timesheet.employee} ({self.timesheet.month:02d}/{self.timesheet.year})"