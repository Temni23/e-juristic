import os
from datetime import datetime
from io import BytesIO

import pdfkit
from django.conf import settings
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from .forms import CourtOrderForm


class HomeView(TemplateView):
    template_name = "documents/home.html"


class DownloadView(TemplateView):
    template_name = "documents/download.html"


def generate_pdf_canvas(request):
    """Генерит PDF файл используя reportlab."""
    if request.method == 'POST':
        form = CourtOrderForm(request.POST)
        if form.is_valid():
            debtor_surname = form.cleaned_data['debtor_surname']
            debtor_name = form.cleaned_data['debtor_name']
            debtor_lastname = form.cleaned_data['debtor_lastname']
            court_number = form.cleaned_data['court_number']
            court_city = form.cleaned_data['court_city']
            debtor_adres = form.cleaned_data['debtor_adres']
            court_order_date = form.cleaned_data['court_order_date']
            court_order_number = form.cleaned_data['court_order_number']
            claimer_name = form.cleaned_data['claimer_name']
            debt_size = form.cleaned_data['debt_size']
            court_order_date_receipt = form.cleaned_data[
                'court_order_date_receipt']

            buffer = BytesIO()
            pdfmetrics.registerFont(TTFont('Arimo', 'static/fonts/Arimo.ttf'))
            pdf = canvas.Canvas(buffer)

            # Add your PDF generation logic here
            pdf.setFont("Arimo", 15)
            pdf.drawString(100, 750,
                           "Фамилия заявителя: {}".format(debtor_surname))
            pdf.drawString(100, 700, "Имя заявителя: {}".format(debtor_name))
            pdf.drawString(100, 650,
                           "Отчество заявителя: {}".format(debtor_lastname))
            pdf.drawString(100, 600,
                           "Номер судебного участка: {}".format(court_number))
            pdf.drawString(100, 550, "Город: {}".format(court_city))
            pdf.drawString(100, 500,
                           "Адрес заявителя: {}".format(debtor_adres))
            pdf.drawString(100, 450,
                           "Дата вынесения судебного приказа: {}".format(
                               court_order_date))
            pdf.drawString(100, 400, "Номер судебного приказа: {}".format(
                court_order_number))
            pdf.drawString(100, 350, "Имя заявителя: {}".format(claimer_name))

            pdf.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True,
                                filename='court_order.pdf')
    else:
        form = CourtOrderForm()
    return render(request, 'documents/court_order_form.html', {'form': form})


def resume_pdf(request, *args, **kwargs):
    """Генерит PDF файл используя wkhtmltopdf."""
    if request.method == 'POST':
        form = CourtOrderForm(request.POST)
        if form.is_valid():
            debtor_surname = form.cleaned_data['debtor_surname']
            debtor_name = form.cleaned_data['debtor_name']
            debtor_lastname = form.cleaned_data['debtor_lastname']
            court_number = form.cleaned_data['court_number']
            court_city = form.cleaned_data['court_city']
            debtor_adres = form.cleaned_data['debtor_adres']
            court_order_date = form.cleaned_data['court_order_date']
            court_order_number = form.cleaned_data['court_order_number']
            claimer_name = form.cleaned_data['claimer_name']
            debt_size = form.cleaned_data['debt_size']
            court_order_date_receipt = form.cleaned_data[
                'court_order_date_receipt']
            wkhtml_to_pdf = os.path.join(
                settings.BASE_DIR, "wkhtmltopdf.exe")
            options = {
                'page-size': 'A4',
                'page-height': "13in",
                'page-width': "10in",
                'margin-top': '1in',
                'margin-right': '1in',
                'margin-bottom': '1in',
                'margin-left': '1in',
                'encoding': "UTF-8",
                'footer-right': 'Заявление подготовлено на сайте e-juristic.ru',
                'footer-font-name': 'Georgia Italic',
                'footer-font-size': '10',
            }

            template_path = 'documents/user_printer.html'
            template = get_template(template_path)  # request.path для текущего пути
            date_create = datetime.now()

            context = {
                "debtor_surname": debtor_surname,
                "debtor_name": debtor_name,
                "debtor_lastname": debtor_lastname,
                "court_number": court_number,
                "court_city": court_city,
                "debtor_adres": debtor_adres,
                "court_order_data": court_order_date,
                "court_order_number": court_order_number,
                "claimer_name": claimer_name,
                "debt_size": debt_size,
                "court_order_date_receipt": court_order_date_receipt,
                "date_create": date_create.date(),
            }
            html = template.render(context)

            config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)

            pdf = pdfkit.from_string(html, False, configuration=config, options=options)

            # Generate download
            response = HttpResponse(pdf, content_type='application/pdf')

            response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
            # print(response.status_code)
            if response.status_code != 200:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

    else:
        form = CourtOrderForm()
    return render(request, 'documents/court_order_form.html', {'form': form})
