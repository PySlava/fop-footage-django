from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from employees.models import Employee
from .services.labor_contract import generate_labor_contract_docx
from .services.unified_report import generate_basic_unified_tax_report_xml
from .services.dps_xml_generator import generate_dps_f3001003_xml
from .services.employment_notice import generate_employment_notice_docx


def _parse_date_safe(date_str):
    """Допоміжна функція для безпечного парсингу дат з QueryParams"""
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    return datetime.now().date()


def notice_list_view(request):
    """Список працівників для завантаження повідомлень"""
    employees = Employee.objects.select_related('fop').all()
    return render(request, 'reports/notice_list.html', {'employees': employees})


def download_employment_notice_view(request, employee_id):
    """Завантаження Повідомлення про прийняття у форматі Word (.docx)"""
    employee = get_object_or_404(Employee, pk=employee_id)
    buffer = generate_employment_notice_docx(employee)

    filename = f"Povidomlennya_{employee.full_name.replace(' ', '_')}.docx"

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def download_dps_notification_xml(request, employee_id):
    """Генерація та завантаження XML для ДПС з апки reports"""
    employee = get_object_or_404(Employee, pk=employee_id)

    fop = getattr(employee, 'fop', None)
    fop_tin = getattr(fop, 'tin', '1234567890') if fop else '1234567890'
    fop_name = getattr(fop, 'full_name', 'ФОП Петренко П.П.') if fop else 'ФОП Петренко П.П.'
    tax_office_code = '2650'

    order_num = request.GET.get('order_num', '1-К')
    order_date = _parse_date_safe(request.GET.get('order_date'))
    start_date = _parse_date_safe(request.GET.get('start_date'))

    xml_buffer = generate_dps_f3001003_xml(
        fop_tin=fop_tin,
        fop_name=fop_name,
        tax_office_code=tax_office_code,
        employee=employee,
        order_num=order_num,
        order_date=order_date,
        start_date=start_date
    )

    filename = f"F3001003_{fop_tin}_{getattr(employee, 'tax_id', '0000000000')}.xml"
    response = HttpResponse(xml_buffer.getvalue(), content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def download_unified_report_xml(request):
    """Експорт XML Об'єднаного розрахунку ПДФО/ВЗ/ЄСВ"""
    company_info = {'tin': '1234567890', 'name': 'ФОП Петренко П.П.', 'month': 9, 'year': 2026}
    salary_records = []
    xml_data = generate_basic_unified_tax_report_xml(company_info, salary_records)
    response = HttpResponse(xml_data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="F0500109_Unified.xml"'
    return response

def download_labor_contract_view(request, employee_id):
    """View для завантаження Трудового договору (.docx)"""
    employee = get_object_or_404(Employee, pk=employee_id)
    buffer = generate_labor_contract_docx(employee)

    filename = f"Trudovyi_Dohovir_{employee.full_name.replace(' ', '_')}.docx"
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


from .services.orders_docx import (
    generate_leave_order_docx,
    generate_business_trip_order_docx,
    generate_salary_change_order_docx,
    generate_financial_aid_order_docx,
)

def download_order_docx_view(request, employee_id, order_type):
    """Генерація та вивантаження кадрових наказів за типом"""
    employee = get_object_or_404(Employee, pk=employee_id)

    order_generators = {
        'leave': (generate_leave_order_docx, "Nakaz_Vidpustka"),
        'trip': (generate_business_trip_order_docx, "Nakaz_Vidryadzhennya"),
        'salary': (generate_salary_change_order_docx, "Nakaz_Oklad"),
        'aid': (generate_financial_aid_order_docx, "Nakaz_Dopomoha"),
    }

    if order_type not in order_generators:
        return HttpResponse("Невідомий тип наказу", status=400)

    generator_func, prefix = order_generators[order_type]
    buffer = generator_func(employee)

    filename = f"{prefix}_{employee.full_name.replace(' ', '_')}.docx"
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

