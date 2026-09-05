import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO


def generate_basic_unified_tax_report_xml(company_info: dict, salary_records: list) -> bytes:
    """
    Формує базову структуру Об'єднаного розрахунку (Додаток 4DF / Додаток 1).
    """
    declar = ET.Element('DECLAR', {
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:noNamespaceSchemaLocation': 'F0500109.xsd'
    })

    head = ET.SubElement(declar, 'DECLARHEAD')
    ET.SubElement(head, 'C_DOC').text = "F05"
    ET.SubElement(head, 'C_DOC_SUB').text = "001"
    ET.SubElement(head, 'C_DOC_VER').text = "9"
    ET.SubElement(head, 'TIN').text = str(company_info.get('tin'))
    ET.SubElement(head, 'PERIOD_MONTH').text = str(company_info.get('month'))
    ET.SubElement(head, 'PERIOD_YEAR').text = str(company_info.get('year'))

    body = ET.SubElement(declar, 'DECLARBODY')
    ET.SubElement(body, 'HTIN').text = str(company_info.get('tin'))
    ET.SubElement(body, 'HNAME').text = str(company_info.get('name'))

    # Підсумок по зарплаті та податках
    total_gross = sum(s.gross_salary for s in salary_records)
    total_pdfo = sum(s.pdfo for s in salary_records)
    total_vz = sum(s.vz for s in salary_records)

    ET.SubElement(body, 'R01G1D').text = f"{total_gross:.2f}"
    ET.SubElement(body, 'R02G1D').text = f"{total_pdfo:.2f}"
    ET.SubElement(body, 'R03G1D').text = f"{total_vz:.2f}"

    buffer = BytesIO()
    tree = ET.ElementTree(declar)
    tree.write(buffer, encoding='windows-1251', xml_declaration=True)
    return buffer.getvalue()