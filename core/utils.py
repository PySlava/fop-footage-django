from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile

def generate_pdf_from_template(template_src, context_dict):
    html_string = render_to_string(template_src, context_dict)
    pdf_bytes = HTML(string=html_string).write_pdf()
    return pdf_bytes