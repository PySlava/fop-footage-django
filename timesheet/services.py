import calendar
from datetime import date
from django.db import transaction
from .models import Timesheet, TimesheetDay


def generate_timesheet(employee, month: int, year: int) -> Timesheet:
    _, days_in_month = calendar.monthrange(year, month)

    is_main_job = getattr(employee, 'employment_type', 'main') == 'main'
    daily_norm_hours = 8 if is_main_job else 4

    with transaction.atomic():
        timesheet, created = Timesheet.objects.get_or_create(
            employee=employee,
            month=month,
            year=year,
            defaults={'status': Timesheet.Status.DRAFT}
        )

        if not created and timesheet.status == Timesheet.Status.APPROVED:
            raise ValueError("Затверджений табель не можна редагувати або перегенеровувати.")

        total_hours = 0
        norm_hours = 0

        for day in range(1, days_in_month + 1):
            current_date = date(year, month, day)
            is_weekend = current_date.weekday() >= 5  # 5 = Субота, 6 = Неділя

            if is_weekend:
                day_type = TimesheetDay.DayType.WEEKEND
                hours = 0
            else:
                day_type = TimesheetDay.DayType.WORK
                hours = daily_norm_hours
                norm_hours += daily_norm_hours

            total_hours += hours

            TimesheetDay.objects.update_or_create(
                timesheet=timesheet,
                date=current_date,
                defaults={
                    'day_type': day_type,
                    'hours': hours,
                }
            )

        timesheet.norm_hours = norm_hours
        timesheet.total_hours = total_hours
        timesheet.save()

    return timesheet