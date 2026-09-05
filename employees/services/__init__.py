from .order_generator import (
    generate_hiring_order_docx,
    generate_dismissal_order_docx,
)

# Аліас на випадок, якщо десь у коді залишилася стара назва функції
generate_employee_order_docx = generate_hiring_order_docx