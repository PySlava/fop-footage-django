from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
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