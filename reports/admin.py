from django.contrib import admin
from django.utils.html import format_html
from .models import TaxReport


@admin.register(TaxReport)
class TaxReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'period_month', 'period_year', 'status', 'created_at', 'download_link')
    list_filter = ('report_type', 'status', 'period_year')

    def download_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" download>Завантажити XML</a>', obj.file.url)
        return "-"
    download_link.short_description = "Файл"