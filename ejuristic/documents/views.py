from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, FormView
from reportlab.platypus import Paragraph, Table, TableStyle, Image

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.shortcuts import render
from django.views.generic import FormView
from xhtml2pdf.files import pisaFileObject

from .forms import CourtOrderForm
from django.http import FileResponse, response
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'static/fonts/Arial.ttf'))


class HomeView(TemplateView):
    template_name = "documents/home.html"


class DownloadView(TemplateView):
    template_name = "documents/download.html"


def generate_pdf_canvas(request):
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
            pdf = canvas.Canvas(buffer)

            # Add your PDF generation logic here
            pdf.setFont("Arial", 32)
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
