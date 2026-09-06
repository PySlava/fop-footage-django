from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from timesheet.models import Timesheet
from employees.models import Employee
from .models import SalaryCalculation
from .services import (
    calculate_salary_for_timesheet,
    get_average_daily_wage,
    calculate_vacation_pay,
    calculate_sick_pay
)
from .services_pdf import generate_payslip_pdf


def salary_list_view(request):
    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    timesheets = Timesheet.objects.filter(
        month=selected_month,
        year=selected_year
    ).select_related('employee', 'salary_calculation')

    salaries = [
        ts.salary_calculation
        for ts in timesheets
        if hasattr(ts, 'salary_calculation') and ts.salary_calculation
    ]

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
            calculate_salary_for_timesheet(ts, ts.employee.salary)
            count += 1

        messages.success(
            request,
            f"Успішно розраховано заробітну плату для {count} працівників за {selected_month:02d}/{selected_year}."
        )
        return redirect(f"/salary/?month={selected_month}&year={selected_year}")

    return redirect('salary:list')


def download_payslip_pdf_view(request, pk):
    """Завантаження розрахункового листка у PDF"""
    salary_calc = get_object_or_404(SalaryCalculation, pk=pk)
    pdf_buffer = generate_payslip_pdf(salary_calc)

    employee_name = salary_calc.timesheet.employee.full_name.replace(' ', '_')
    filename = f"Payslip_{employee_name}_{salary_calc.timesheet.month:02d}_{salary_calc.timesheet.year}.pdf"

    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def vacation_sick_calculator_view(request):
    """Інтегрований калькулятор відпускних та лікарняних"""
    employees = Employee.objects.all()
    now = datetime.now()

    result = None
    selected_employee = None
    calc_type = request.GET.get('calc_type', 'vacation')
    days = int(request.GET.get('days', 14))
    exp_years = int(request.GET.get('exp_years', 8))
    emp_id = request.GET.get('employee')

    if emp_id:
        selected_employee = get_object_or_404(Employee, pk=emp_id)
        avg_info = get_average_daily_wage(selected_employee, now.month, now.year)

        if calc_type == 'vacation':
            calc_data = calculate_vacation_pay(avg_info['avg_daily_wage'], days)
        else:
            calc_data = calculate_sick_pay(avg_info['avg_daily_wage'], days, exp_years)

        result = {
            'avg_info': avg_info,
            'calc_data': calc_data,
            'calc_type': calc_type,
        }

    return render(request, 'salary/calculator.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'result': result,
        'calc_type': calc_type,
        'days': days,
        'exp_years': exp_years,
    })