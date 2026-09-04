from django.db import transaction
from django.utils import timezone
from documents.models import HiringOrder
from dps_reports.models import DpsNotification
from core.utils import generate_pdf_from_template
from django.core.files.base import ContentFile


class EmployeeCreationService:
    @staticmethod
    @transaction.atomic
    def create_employee_with_automation(form_data):
        employee = form_data.save()

        order_count = HiringOrder.objects.filter(employee__fop=employee.fop).count() + 1
        order_num = f"{order_count}-К"

        pdf_bytes = generate_pdf_from_template('documents/pdf/hiring_order_pdf.html', {
            'employee': employee,
            'fop': employee.fop,
            'order_number': order_num,
            'order_date': employee.hire_date,
        })

        hiring_order = HiringOrder.objects.create(
            employee=employee,
            order_number=order_num,
            order_date=employee.hire_date
        )
        hiring_order.pdf_file.save(f"nakaz_{employee.tax_id}.pdf", ContentFile(pdf_bytes))

        DpsNotification.objects.create(
            employee=employee,
            status='draft'
        )

        return employee