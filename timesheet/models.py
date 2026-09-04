from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from employees.models import Employee


class Timesheet(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновий'
        APPROVED = 'approved', 'Затверджений'

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='timesheet',
        verbose_name='Працівник',
    )
    month = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='Місяць'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Рік'
    )
    norm_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Норма годин'
    )
    total_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Відпрацьовано годин'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Табель'
        verbose_name_plural = 'Табелі'
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
        return f"Табель {self.employee} - {self.month:02d}/{self.year}"


class TimesheetDay(models.Model):
    class DayType(models.TextChoices):
        WORK = 'WORK', 'Робочий'
        WEEKEND = 'WEEKEND', 'Вихідний'
        VACATION = 'VACATION', 'Відпустка'
        SICK = 'SICK', 'Лікарняний'

    timesheet = models.ForeignKey(
        Timesheet,
        on_delete=models.CASCADE,
        related_name='days',
        verbose_name='Табель'
    )
    date = models.DateField(verbose_name='Дата')
    day_type = models.CharField(
        max_length=10,
        choices=DayType.choices,
        default=DayType.WORK,
        verbose_name='Тип дня'
    )
    hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        verbose_name='Години'
    )

    class Meta:
        verbose_name = 'День табеля'
        verbose_name_plural = 'Дні табеля'
        ordering = ['date']
        unique_together = ('timesheet', 'date')

    def __str__(self):
        return f"{self.date}: {self.day_type} ({self.hours}г)"