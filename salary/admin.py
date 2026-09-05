from django.contrib import admin
from .models import SalaryCalculation

@admin.register(SalaryCalculation)
class SalaryCalculationAdmin(admin.ModelAdmin):
    list_display = (
        'get_employee',
        'get_period',
        'base_salary',
        'worked_hours',
        'gross_salary',
        'pdfo',
        'vz',
        'net_salary',
        'esv',
    )
    list_filter = ('timesheet__year', 'timesheet__month')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Працівник')
    def get_employee(self, obj):
        return obj.timesheet.employee.full_name

    @admin.display(description='Період')
    def get_period(self, obj):
        return f"{obj.timesheet.month:02d}/{obj.timesheet.year}"