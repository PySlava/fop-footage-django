from django.contrib import admin
from .models import Fops


@admin.register(Fops)
class FopsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'tax_id', 'city', 'tax_system', 'main_kved', 'dps_code')
    search_fields = ('full_name', 'tax_id', 'city', 'katottg')

    fieldsets = (
        ('Основні дані', {
            'fields': ('full_name', 'tax_id', 'opf_code')
        }),
        ('Адреса реєстрації (прописка)', {
            'fields': ('postal_code', 'region', 'district', 'city', 'katottg', 'street', 'building')
        }),
        ('Діяльність та податки', {
            'fields': ('main_kved', 'additional_kveds', 'tax_system')
        }),
        ('Органи обліку (ДПС / ПФУ)', {
            'fields': ('dps_code', 'dps_name', 'pfu_code')
        }),
    )