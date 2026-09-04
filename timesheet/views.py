from django.shortcuts import render

from django.shortcuts import get_object_or_404
from .models import Timesheet
from .exports import export_timesheet_to_excel

def export_timesheet_view(request, timesheet_id):
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)
    return export_timesheet_to_excel(timesheet)
