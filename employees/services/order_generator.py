import io
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


def generate_hiring_order_docx(employee, order_num, order_date, start_date):
    """Генерує наказ про прийняття на роботу (.docx)"""
    doc = Document()
    fop = employee.fop
    fop_name = fop.full_name if fop else "ФОП Роботодавець"

    # Шапка
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_head.add_run(f"Затверджено\n{fop_name}\n").bold = True

    # Заголовок
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(18)
    run_title = p_title.add_run(f"НАКАЗ № {order_num}\nпро прийняття на роботу")
    run_title.bold = True
    run_title.font.size = Pt(14)

    # Дата та місто
    p_meta = doc.add_paragraph()
    p_meta.add_run(f"м. Київ                                                                        {order_date.strftime('%d.%m.%Y')} р.\n\n")

    # Текст наказу
    p_body = doc.add_paragraph()
    p_body.paragraph_format.line_spacing = 1.15
    p_body.add_run(
        f"ПРИЙНЯТИ {employee.full_name} (ІПН: {employee.tax_id}) на роботу "
        f"з {start_date.strftime('%d.%m.%Y')} року на умовах основного місця роботи.\n\n"
        f"Підстава: Заява працівника, трудовий договір."
    )

    # Підпис
    doc.add_paragraph("\n\n")
    p_sign = doc.add_paragraph()
    p_sign.add_run(f"ФОП: ___________________  / {fop_name} /\n\n")
    p_sign.add_run(f"З наказом ознайомлений(а): ___________________  / {employee.full_name} /")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def generate_dismissal_order_docx(employee, order_num, order_date, dismissal_date):
    """Генерує наказ про звільнення за згодою сторін (.docx)"""
    doc = Document()
    fop = employee.fop
    fop_name = fop.full_name if fop else "ФОП Роботодавець"

    # Заголовок
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(18)
    run_title = p_title.add_run(f"НАКАЗ № {order_num}\nпро звільнення за згодою сторін")
    run_title.bold = True
    run_title.font.size = Pt(14)

    p_meta = doc.add_paragraph()
    p_meta.add_run(f"м. Київ                                                                        {order_date.strftime('%d.%m.%Y')} р.\n\n")

    p_body = doc.add_paragraph()
    p_body.paragraph_format.line_spacing = 1.15
    p_body.add_run(
        f"ЗВІЛЬНИТИ {employee.full_name} (ІПН: {employee.tax_id}) з посади "
        f"{dismissal_date.strftime('%d.%m.%Y')} року за згодою сторін, п. 1 ст. 36 КЗпП України.\n\n"
        f"Підстава: Заява працівника від {order_date.strftime('%d.%m.%Y')} року."
    )

    doc.add_paragraph("\n\n")
    p_sign = doc.add_paragraph()
    p_sign.add_run(f"ФОП: ___________________  / {fop_name} /\n\n")
    p_sign.add_run(f"З наказом ознайомлений(а): ___________________  / {employee.full_name} /")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer