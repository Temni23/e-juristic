import weasyprint
from django.template.loader import render_to_string


def draw_ticket_to_pdf(context: dict) -> bytes:
    """Формирует файл в формате PDF и возвращает его."""
    rendered_html = render_to_string('../templates/documents/user_printer.html',
                                     context=context)

    pdf = weasyprint.HTML(string=rendered_html).write_pdf()

    return pdf
