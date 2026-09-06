import calendar
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.db.models import Sum
from .models import SalaryCalculation

PDFO_RATE = Decimal('0.18')
VZ_RATE = Decimal('0.05')
ESV_RATE = Decimal('0.22')
MIN_SALARY = Decimal('8000.00')


def quantize_money(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_salary_for_timesheet(timesheet, base_salary: Decimal) -> SalaryCalculation:
    if timesheet.norm_hours == 0:
        raise ValueError("Норма годин у табелі не може дорівнювати нулю.")

    base_salary = Decimal(str(base_salary))
    norm_hours = Decimal(str(timesheet.norm_hours))
    worked_hours = Decimal(str(timesheet.total_hours))

    gross_salary = quantize_money(base_salary * (worked_hours / norm_hours))

    pdfo = quantize_money(gross_salary * PDFO_RATE)
    vz = quantize_money(gross_salary * VZ_RATE)

    net_salary = gross_salary - pdfo - vz

    calculated_esv = quantize_money(gross_salary * ESV_RATE)

    is_main_job = getattr(timesheet.employee, 'employment_type', 'main') == 'main'
    min_esv = quantize_money(MIN_SALARY * ESV_RATE)

    if is_main_job and worked_hours > 0 and calculated_esv < min_esv:
        esv = min_esv
    else:
        esv = calculated_esv

    with transaction.atomic():
        salary_calc, _ = SalaryCalculation.objects.update_or_create(
            timesheet=timesheet,
            defaults={
                'base_salary': base_salary,
                'norm_hours': norm_hours,
                'worked_hours': worked_hours,
                'gross_salary': gross_salary,
                'pdfo': pdfo,
                'vz': vz,
                'esv': esv,
                'net_salary': net_salary,
            }
        )

    return salary_calc


# --- РОЗРАХУНОК ВІДПУСКНИХ ТА ЛІКАРНЯНИХ (ПОРЯДОК № 100 та № 1266) ---

def get_average_daily_wage(employee, target_month: int, target_year: int) -> dict:
    """
    Розрахунок середньоденної заробітної плати за останні 12 календарних місяців,
    що передують місяцю нарахування.
    """
    start_month = target_month
    start_year = target_year - 1

    # Знаходимо всі проведені розрахунки ЗП працівника за розрахунковий період (12 місяців)
    calculations = SalaryCalculation.objects.filter(
        timesheet__employee=employee,
    ).select_related('timesheet')

    period_calcs = []
    total_gross = Decimal('0.00')
    total_days = 0

    for calc in calculations:
        ts_date = date(calc.timesheet.year, calc.timesheet.month, 1)
        start_date = date(start_year, start_month, 1)
        end_date = date(target_year, target_month, 1)

        if start_date <= ts_date < end_date:
            period_calcs.append(calc)
            total_gross += calc.gross_salary
            # Кількість календарних днів у місяці
            _, days_in_month = calendar.monthrange(calc.timesheet.year, calc.timesheet.month)
            total_days += days_in_month

    if total_days == 0:
        # Якщо немає історії розрахунків за 12 місяців, використовуємо поточний оклад
        base_salary = getattr(employee, 'salary', Decimal('0.00'))
        avg_daily = quantize_money(Decimal(str(base_salary)) / Decimal('30.44'))
        return {
            'total_gross': Decimal('0.00'),
            'total_days': 0,
            'months_count': 0,
            'avg_daily_wage': avg_daily,
            'is_fallback': True
        }

    avg_daily_wage = quantize_money(total_gross / Decimal(total_days))

    return {
        'total_gross': total_gross,
        'total_days': total_days,
        'months_count': len(period_calcs),
        'avg_daily_wage': avg_daily_wage,
        'is_fallback': False
    }


def calculate_vacation_pay(avg_daily_wage: Decimal, vacation_days: int) -> dict:
    """Розрахунок відпускних: Середньоденна ЗП * Кількість днів відпустки"""
    total = quantize_money(avg_daily_wage * Decimal(vacation_days))
    pdfo = quantize_money(total * PDFO_RATE)
    vz = quantize_money(total * VZ_RATE)
    net = total - pdfo - vz
    esv = quantize_money(total * ESV_RATE)

    return {
        'days': vacation_days,
        'total_gross': total,
        'pdfo': pdfo,
        'vz': vz,
        'net': net,
        'esv': esv
    }


def calculate_sick_pay(avg_daily_wage: Decimal, sick_days: int, experience_years: int = 8) -> dict:
    """
    Розрахунок лікарняних за страховим стажем:
    - до 3 років: 50%
    - 3 - 5 років: 60%
    - 5 - 8 років: 70%
    - понад 8 років: 100%
    """
    if experience_years < 3:
        percent = Decimal('0.50')
    elif experience_years < 5:
        percent = Decimal('0.60')
    elif experience_years < 8:
        percent = Decimal('0.70')
    else:
        percent = Decimal('1.00')

    daily_amount = quantize_money(avg_daily_wage * percent)
    total = quantize_money(daily_amount * Decimal(sick_days))

    # Перші 5 днів сплачує роботодавець, решту — ПФУ
    employer_days = min(sick_days, 5)
    pension_fund_days = max(0, sick_days - 5)

    employer_amount = quantize_money(daily_amount * Decimal(employer_days))
    pension_fund_amount = quantize_money(daily_amount * Decimal(pension_fund_days))

    pdfo = quantize_money(total * PDFO_RATE)
    vz = quantize_money(total * VZ_RATE)
    net = total - pdfo - vz
    esv = quantize_money(total * ESV_RATE)

    return {
        'days': sick_days,
        'percent': int(percent * 100),
        'total_gross': total,
        'employer_amount': employer_amount,
        'pension_fund_amount': pension_fund_amount,
        'pdfo': pdfo,
        'vz': vz,
        'net': net,
        'esv': esv
    }