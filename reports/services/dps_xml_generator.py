import io
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime


def generate_dps_f3001003_xml(fop_tin, fop_name, tax_office_code, employee, order_num, order_date, start_date,
                              doc_num=1):
    """
    Генерує XML-файл форми F3001003 (Повідомлення про прийняття працівника на роботу)
    згідно зі стандартом ДПС України.
    """
    today = datetime.now()

    root = ET.Element("DECLARATION")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "F3001003.xsd")

    # Службова заголовочна частина (DECLARHEAD)
    head = ET.SubElement(root, "DECLARHEAD")
    ET.SubElement(head, "C_DOC").text = "F30"
    ET.SubElement(head, "C_DOC_SUB").text = "010"
    ET.SubElement(head, "C_DOC_VER").text = "3"
    ET.SubElement(head, "C_DOC_STAN").text = "1"  # 1 - звітна
    ET.SubElement(head, "C_DOC_TYPE").text = "0"
    ET.SubElement(head, "C_DOC_NUM").text = str(doc_num)
    ET.SubElement(head, "C_DS").text = today.strftime("%m")

    # Коди ДПС (область / район)
    reg_code = tax_office_code[:2] if len(tax_office_code) >= 2 else "26"
    raj_code = tax_office_code[2:] if len(tax_office_code) >= 4 else "50"
    ET.SubElement(head, "C_REG").text = reg_code
    ET.SubElement(head, "C_RAJ").text = raj_code

    ET.SubElement(head, "PERIOD_MONTH").text = str(today.month)
    ET.SubElement(head, "PERIOD_TYPE").text = "1"  # місяць
    ET.SubElement(head, "PERIOD_YEAR").text = str(today.year)
    ET.SubElement(head, "D_FILL").text = today.strftime("%d%m%Y")
    ET.SubElement(head, "HKSEL").text = str(fop_tin)
    ET.SubElement(head, "HNAME").text = str(fop_name)
    ET.SubElement(head, "HSTI").text = str(tax_office_code)

    # Змістовна частина (DECLARBODY)
    body = ET.SubElement(root, "DECLARBODY")
    ET.SubElement(body, "HKSEL").text = str(fop_tin)
    ET.SubElement(body, "HNAME").text = str(fop_name)

    # Рядок 1 з даними працівника
    ET.SubElement(body, "T1RXXXXG1S").text = "1"  # № з/п
    ET.SubElement(body, "T1RXXXXG2").text = str(getattr(employee, 'insured_category', '1'))
    ET.SubElement(body, "T1RXXXXG3S").text = str(getattr(employee, 'tax_id', ''))
    ET.SubElement(body, "T1RXXXXG4S").text = str(employee.full_name)
    ET.SubElement(body, "T1RXXXXG5S").text = str(order_num)
    ET.SubElement(body, "T1RXXXXG6D").text = order_date.strftime("%d%m%Y")
    ET.SubElement(body, "T1RXXXXG7D").text = start_date.strftime("%d%m%Y")
    ET.SubElement(body, "T1RXXXXG8").text = "1" if getattr(employee, 'is_ukrainian_citizen', True) else "0"

    ET.SubElement(body, "HFILL").text = today.strftime("%d%m%Y")
    ET.SubElement(body, "HBOSS").text = str(fop_name)

    # Форматування XML
    raw_xml = ET.tostring(root, encoding="windows-1251")
    parsed = minidom.parseString(raw_xml)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="windows-1251")

    buffer = io.BytesIO()
    buffer.write(pretty_xml)
    buffer.seek(0)
    return buffer