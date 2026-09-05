from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import EmployeeForm
from .models import Employee, Order
from .services.order_generator import (
    generate_hiring_order_docx,
    generate_dismissal_order_docx,
)


def employee_list_view(request):
    """Список працівників"""
    employees = Employee.objects.select_related('fop').all().order_by('-hire_date')
    return render(request, 'employees/employee_list.html', {
        'employees': employees
    })


def employee_create_view(request):
    """Створення працівника"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees:list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form
    })


def employee_actions_view(request, pk):
    """Сторінка дій з працівником (форми для генерації наказів про прийняття / звільнення)"""
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        order_num = request.POST.get('order_num', '1-К')
        order_date_str = request.POST.get('order_date')
        target_date_str = request.POST.get('target_date')

        order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date() if order_date_str else datetime.now().date()
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date() if target_date_str else order_date

        if action_type == 'hire':
            # Зберігаємо в журнал
            Order.objects.create(
                employee=employee,
                order_type='hire',
                order_num=order_num,
                order_date=order_date,
                effective_date=target_date
            )
            employee.hire_date = target_date
            employee.is_active = True
            employee.save()

            buffer = generate_hiring_order_docx(employee, order_num, order_date, target_date)
            filename = f"Nakaz_Pryynyattya_{employee.full_name.replace(' ', '_')}.docx"
            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        elif action_type == 'dismissal':
            Order.objects.create(
                employee=employee,
                order_type='dismissal_agreement',
                order_num=order_num,
                order_date=order_date,
                effective_date=target_date
            )
            employee.dismissal_date = target_date
            employee.is_active = False
            employee.save()

            buffer = generate_dismissal_order_docx(employee, order_num, order_date, target_date)
            filename = f"Nakaz_Zvilnennya_{employee.full_name.replace(' ', '_')}.docx"
            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

    return render(request, 'employees/employee_actions.html', {'employee': employee})


def orders_list_view(request):
    """Журнал ведення реєстру наказів"""
    orders = Order.objects.select_related('employee', 'employee__fop').order_by('-order_date')
    return render(request, 'employees/orders_list.html', {'orders': orders})