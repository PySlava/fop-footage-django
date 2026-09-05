from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from employees.models import Employee
from .services.employment_notice import generate_employment_notice_docx


def notice_list_view(request):
    """Список працівників для завантаження повідомлень"""
    employees = Employee.objects.select_related('fop').all()
    return render(request, 'reports/notice_list.html', {'employees': employees})


def download_employment_notice_view(request, pk):
    """Завантаження Повідомлення про прийняття у форматі Word (.docx)"""
    employee = get_object_or_404(Employee, pk=pk)
    buffer = generate_employment_notice_docx(employee)

    filename = f"Povidomlennya_{employee.full_name.replace(' ', '_')}.docx"

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response