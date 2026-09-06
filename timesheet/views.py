from datetime import datetime
from django.shortcuts import render
from employees.models import Employee
from .services.excel_export import generate_timesheet_p5_xlsx
from .models import Timesheet, TimesheetDay

def timesheet_list_view(request):
    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    employees = Employee.objects.select_related('fop').filter(is_active=True)

    # Отримуємо існуючі табелі за обраний місяць та рік разом із днями
    timesheets = Timesheet.objects.filter(
        month=selected_month,
        year=selected_year
    ).select_related('employee').prefetch_related('days')

    timesheet_map = {ts.employee_id: ts for ts in timesheets}

    employee_timesheets = []
    for emp in employees:
        ts = timesheet_map.get(emp.id)

        if ts:
            # Рахуємо дні з пов'язаних записів TimesheetDay
            sick_days = ts.days.filter(day_type=TimesheetDay.DayType.SICK).count()
            vacation_days = ts.days.filter(day_type=TimesheetDay.DayType.VACATION).count()
            work_days = ts.days.filter(day_type=TimesheetDay.DayType.WORK).count()
        else:
            sick_days = 0
            vacation_days = 0
            work_days = 0

        employee_timesheets.append({
            'employee': emp,
            'timesheet': ts,
            'norm_hours': ts.norm_hours if ts else 168.00,
            'total_hours': ts.total_hours if ts else 0.00,
            'work_days': work_days,
            'sick_days': sick_days,
            'vacation_days': vacation_days,
        })

    months_list = [
        (1, 'Січень'), (2, 'Лютий'), (3, 'Березень'), (4, 'Квітень'),
        (5, 'Травень'), (6, 'Червень'), (7, 'Липень'), (8, 'Серпень'),
        (9, 'Вересень'), (10, 'Жовтень'), (11, 'Листопад'), (12, 'Грудень')
    ]

    return render(request, 'timesheet/timesheet_list.html', {
        'employee_timesheets': employee_timesheets,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months_list': months_list,
        'years_list': range(now.year - 2, now.year + 2),
    })

def download_timesheet_xlsx_view(request):
    """View для завантаження Табеля П-5 у форматі .xlsx з модуля timesheet"""
    now = datetime.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    employees = Employee.objects.all().order_by('full_name')
    buffer = generate_timesheet_p5_xlsx(year=year, month=month, employees=employees)

    filename = f"Tabel_P5_{month:02d}_{year}.xlsx"
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

