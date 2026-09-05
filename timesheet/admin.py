from django.contrib import admin
from .models import Timesheet, TimesheetDay

class TimesheetDayInline(admin.TabularInline):
    model = TimesheetDay
    extra = 0
    ordering = ['date']

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'norm_hours', 'total_hours', 'status')
    list_filter = ('year', 'month', 'status')
    search_fields = ('employee__full_name',)
    inlines = [TimesheetDayInline]

@admin.register(TimesheetDay)
class TimesheetDayAdmin(admin.ModelAdmin):
    list_display = ('timesheet', 'date', 'day_type', 'hours')
    list_filter = ('day_type', 'date')