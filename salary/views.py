from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from timesheet.models import Timesheet
from .models import SalaryCalculation
from .services import calculate_salary_for_timesheet

def salary_list_view(request):
    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    # Отримуємо всі табелі за період разом із прив'язаними розрахунками ЗП
    timesheets = Timesheet.objects.filter(
        month=selected_month,
        year=selected_year
    ).select_related('employee', 'salary_calculation')

    # Формуємо список існуючих розрахунків для підсумків
    salaries = [
        ts.salary_calculation
        for ts in timesheets
        if hasattr(ts, 'salary_calculation') and ts.salary_calculation
    ]

    # Обчислюємо загальні підсумки відомості
    totals = {
        'gross': sum(s.gross_salary for s in salaries),
        'pdfo': sum(s.pdfo for s in salaries),
        'vz': sum(s.vz for s in salaries),
        'esv': sum(s.esv for s in salaries),
        'net': sum(s.net_salary for s in salaries),
    }

    months_list = [
        (1, 'Січень'), (2, 'Лютий'), (3, 'Березень'), (4, 'Квітень'),
        (5, 'Травень'), (6, 'Червень'), (7, 'Липень'), (8, 'Серпень'),
        (9, 'Вересень'), (10, 'Жовтень'), (11, 'Листопад'), (12, 'Грудень')
    ]

    return render(request, 'salary/salary_list.html', {
        'timesheets': timesheets,
        'totals': totals,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months_list': months_list,
        'years_list': range(now.year - 2, now.year + 2),
    })

def calculate_salaries_view(request):
    """Масовий розрахунок зарплати за вибраний місяць"""
    if request.method == 'POST':
        selected_month = int(request.POST.get('month'))
        selected_year = int(request.POST.get('year'))

        timesheets = Timesheet.objects.filter(
            month=selected_month,
            year=selected_year
        ).select_related('employee')

        if not timesheets.exists():
            messages.warning(request, f"За {selected_month:02d}/{selected_year} не знайдено жодного табеля.")
            return redirect(f"/salary/?month={selected_month}&year={selected_year}")

        count = 0
        for ts in timesheets:
            # Оклад береться безпосередньо з моделі Employee
            calculate_salary_for_timesheet(ts, ts.employee.salary)
            count += 1

        messages.success(
            request,
            f"Успішно розраховано заробітну плату для {count} працівників за {selected_month:02d}/{selected_year}."
        )
        return redirect(f"/salary/?month={selected_month}&year={selected_year}")

    return redirect('salary:list')