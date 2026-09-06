import calendar
import io
from datetime import datetime
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


def generate_timesheet_p5_xlsx(year=None, month=None, employees=None):
    """
    Генерує Табель обліку робочого часу (Форма П-5) у форматі .xlsx
    """
    now = datetime.now()
    year = year or now.year
    month = month or now.month

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Табель {month:02d}.{year}"

    # Налаштування стилів
    font_header = Font(name="Calibri", size=9, bold=True)
    font_cell = Font(name="Calibri", size=9)
    font_title = Font(name="Calibri", size=12, bold=True)

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")

    fill_weekend = PatternFill(start_color="F2D7D5", end_color="F2D7D5", fill_type="solid")
    fill_header = PatternFill(start_color="EAECEE", end_color="EAECEE", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="D0D3D4"),
        right=Side(style="thin", color="D0D3D4"),
        top=Side(style="thin", color="D0D3D4"),
        bottom=Side(style="thin", color="D0D3D4")
    )

    # Заголовок формату П-5
    ws.merge_cells("A1:AJ1")
    ws["A1"] = f"ТАБЕЛЬ ОБЛІКУ ВИКОРИСТАННЯ РОБОЧОГО ЧАСУ за {month:02d}.{year} року"
    ws["A1"].font = font_title
    ws["A1"].alignment = align_center

    # Заголовки таблиці
    headers = ["№", "ПІБ Працівника", "Посада", "Таб. №"]
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        headers.append(str(day))

    headers.extend(["Відпр. днів", "Відпр. годин"])

    # Запис шапки
    ws.row_dimensions[3].height = 25
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col_idx, value=header)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = thin_border

    # Наповнення даними
    start_row = 4
    employees = employees or []

    for idx, emp in enumerate(employees, start=1):
        row = start_row + (idx - 1)
        ws.row_dimensions[row].height = 20

        pos = getattr(emp, 'position', 'Працівник')
        emp_id = getattr(emp, 'id', idx)

        ws.cell(row=row, column=1, value=idx).alignment = align_center
        ws.cell(row=row, column=2, value=emp.full_name).alignment = align_left
        ws.cell(row=row, column=3, value=pos).alignment = align_left
        ws.cell(row=row, column=4, value=f"{emp_id:04d}").alignment = align_center

        total_days = 0
        total_hours = 0

        for day in range(1, days_in_month + 1):
            col_idx = 4 + day
            date_obj = datetime(year, month, day)
            is_weekend = date_obj.weekday() in (5, 6)

            cell = ws.cell(row=row, column=col_idx)

            if is_weekend:
                cell.value = "В"
                cell.fill = fill_weekend
            else:
                cell.value = "Р / 8"
                total_days += 1
                total_hours += 8

            cell.alignment = align_center
            cell.font = font_cell
            cell.border = thin_border

        days_col = 4 + days_in_month + 1
        hours_col = 4 + days_in_month + 2

        cell_d = ws.cell(row=row, column=days_col, value=total_days)
        cell_h = ws.cell(row=row, column=hours_col, value=total_hours)

        for c in (cell_d, cell_h):
            c.font = font_header
            c.alignment = align_center
            c.border = thin_border

        for c_idx in range(1, 5):
            ws.cell(row=row, column=c_idx).border = thin_border

    # Ширина колонок
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 18
    ws.column_dimensions['D'].width = 10

    for day in range(1, days_in_month + 1):
        col_letter = get_column_letter(4 + day)
        ws.column_dimensions[col_letter].width = 6

    ws.column_dimensions[get_column_letter(4 + days_in_month + 1)].width = 12
    ws.column_dimensions[get_column_letter(4 + days_in_month + 2)].width = 12

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer