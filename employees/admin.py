from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'tax_id', 'hire_date', 'salary', 'fop')
    search_fields = ('full_name', 'tax_id')
    list_filter = ('fop', 'employment_type')