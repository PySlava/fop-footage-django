import json
from datetime import date
from django.shortcuts import render
from django.db.models import Sum
from salary.models import SalaryCalculation
from timesheet.models import TimesheetDay


def dashboard_index_view(request):
    current_year = date.today().year

    # 1. Агрегація витрат на ФОП та податки по місяцях
    monthly_stats = (
        SalaryCalculation.objects.filter(timesheet__year=current_year)
        .values('timesheet__month')
        .annotate(
            total_gross=Sum('gross_salary'),
            total_pdfo=Sum('pdfo'),
            total_vz=Sum('vz'),
            total_esv=Sum('esv'),
            total_net=Sum('net_salary'),
        )
    )

    months_labels = ['Січ', 'Лют', 'Бер', 'Квіт', 'Трав', 'Черв', 'Лип', 'Серп', 'Верес', 'Жовт', 'Лист', 'Груд']
    fop_series = [0.0] * 12
    taxes_series = [0.0] * 12
    esv_series = [0.0] * 12

    for row in monthly_stats:
        idx = row['timesheet__month'] - 1
        fop_series[idx] = float(row['total_gross'] or 0)
        taxes_series[idx] = float((row['total_pdfo'] or 0) + (row['total_vz'] or 0))
        esv_series[idx] = float(row['total_esv'] or 0)

    # 2. Вибірка відпусток із TimesheetDay за допомогою поля day_type
    vacation_days = TimesheetDay.objects.filter(
        timesheet__year=current_year,
        day_type__in=['V', 'В', 'VACATION', 'vacation', 'відпустка', 'ОП', 'ВП']
    ).select_related('timesheet__employee')

    vacation_events = []
    for day in vacation_days:
        emp_name = day.timesheet.employee.full_name
        # Використовуємо поле date безпосередньо з об'єкта TimesheetDay
        day_date_str = day.date.strftime('%Y-%m-%d')

        vacation_events.append({
            'title': emp_name,
            'start': day_date_str,
            'allDay': True,
            'color': '#0d6efd'
        })

    return render(request, 'dashboard/index.html', {
        'current_year': current_year,
        'months_labels_json': json.dumps(months_labels),
        'fop_series_json': json.dumps(fop_series),
        'taxes_series_json': json.dumps(taxes_series),
        'esv_series_json': json.dumps(esv_series),
        'vacation_events_json': json.dumps(vacation_events),
    })