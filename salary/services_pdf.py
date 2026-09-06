import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Реєстрація стандартного шрифту DejaVuSans для кирилиці
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'https://github.com/google/fonts/raw/main/ofl/dejavusans/DejaVuSans.ttf'))
except Exception:
    pass


def generate_payslip_pdf(salary_calc) -> io.BytesIO:
    """Генерує розрахунковий листок у форматі A5 (горизонтальний)"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A5),
        rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontName='DejaVu',
        fontSize=12,
        leading=14,
        alignment=1,  # Center
        textColor=colors.HexColor('#1A252C')
    )
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName='DejaVu', fontSize=9, leading=11)
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontName='DejaVu', fontSize=9, leading=11)

    employee = salary_calc.timesheet.employee
    month_name = [
        'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
        'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'
    ][salary_calc.timesheet.month - 1]

    elements = []

    # Шапка
    elements.append(
        Paragraph(f"<b>РОЗРАХУНКОВИЙ ЛИСТОК ЗА {month_name.upper()} {salary_calc.timesheet.year} Р.</b>", title_style))
    fop_name = getattr(employee.fop, 'full_name', 'ФОП') if hasattr(employee, 'fop') else 'ФОП'
    elements.append(
        Paragraph(f"<font size=8 color='#555555'>Роботодавець: {fop_name} | Працівник: {employee.full_name}</font>",
                  title_style))
    elements.append(Spacer(1, 10))

    # Таблиця
    data = [
        [
            Paragraph("<b>НАРАХОВАНО</b>", bold_style),
            Paragraph("<b>СУМА (грн)</b>", bold_style),
            Paragraph("<b>УТРИМАНО / НАРАХОВАНО ЄСВ</b>", bold_style),
            Paragraph("<b>СУМА (грн)</b>", bold_style)
        ],
        [
            Paragraph(f"Оклад ({salary_calc.worked_hours}/{salary_calc.norm_hours} год)", text_style),
            f"{salary_calc.gross_salary:.2f}",
            Paragraph("ПДФО (18%)", text_style),
            f"{salary_calc.pdfo:.2f}"
        ],
        [
            Paragraph("", text_style),
            "",
            Paragraph("Військовий збір (5%)", text_style),
            f"{salary_calc.vz:.2f}"
        ],
        [
            Paragraph("<b>Всього нараховано (Gross)</b>", bold_style),
            f"<b>{salary_calc.gross_salary:.2f}</b>",
            Paragraph("<b>Всього утримано</b>", bold_style),
            f"<b>{(salary_calc.pdfo + salary_calc.vz):.2f}</b>"
        ],
        [
            Paragraph("<b>ДО ВИПЛАТИ (Net)</b>", bold_style),
            f"<b>{salary_calc.net_salary:.2f}</b>",
            Paragraph("ЄСВ 22% (сплачує ФОП)", text_style),
            f"{salary_calc.esv:.2f}"
        ]
    ]

    t = Table(data, colWidths=[150, 90, 180, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EAECEE')),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D0D3D4')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#F8F9F9')),
        ('BACKGROUND', (0, 4), (1, 4), colors.HexColor('#D4EFDF')),
    ]))

    elements.append(t)
    doc.build(elements)

    buffer.seek(0)
    return buffer