from django.shortcuts import render, redirect
from employees.forms import EmployeeForm
from employees.models import Employee
from employees.services import EmployeeCreationService


def employee_list(request):
    employees = Employee.objects.select_related('fop').all()
    return render(request, 'employees/employee_list.html', {'employees': employees})


def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})


def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Викликаємо наш бізнес-сервіс замість звичайного form.save()
            EmployeeCreationService.create_employee_with_automation(form)
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})