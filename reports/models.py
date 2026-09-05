from django.db import models


class TaxReport(models.Model):
    class ReportType(models.TextChoices):
        EMPLOYMENT_NOTICE = 'EMPLOYMENT_NOTICE', 'Повідомлення про прийняття працівника'
        UNIFIED_TAX_REPORT = 'UNIFIED_TAX_REPORT', 'Обєднаний звіт (ПДФО/ЄСВ)'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновий'
        GENERATED = 'GENERATED', 'Згенеровано XML'
        SENT = 'SENT', 'Відправлено в ДПС'

    report_type = models.CharField(max_length=30, choices=ReportType.choices, verbose_name="Тип звіту")
    period_month = models.PositiveSmallIntegerField(verbose_name="Місяць")
    period_year = models.PositiveIntegerField(verbose_name="Рік")
    file = models.FileField(upload_to='tax_reports_xml/', null=True, blank=True, verbose_name="XML Файл")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Податковий звіт"
        verbose_name_plural = "Податкові звіти"

    def __str__(self):
        return f"{self.get_report_type_display()} за {self.period_month:02d}/{self.period_year}"