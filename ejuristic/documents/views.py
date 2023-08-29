import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .custom_functions import draw_ticket_to_pdf
from .forms import CourtOrderForm


class HomeView(TemplateView):
    template_name = "documents/home.html"


class DownloadView(TemplateView):
    template_name = "documents/download.html"


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

            # template_path = 'documents/user_printer.html'
            # template = get_template(template_path)  # request.path для текущего пути
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
            # html = template.render(context)
            #
            # config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)
            #
            # pdf = pdfkit.from_string(html, False, configuration=config, options=options)

            pdf = draw_ticket_to_pdf(context)

            # Generate download
            response = HttpResponse(pdf, content_type='application/pdf')

            response[
                'Content-Disposition'] = 'attachment; filename="resume.pdf"'
            # print(response.status_code)
            # if response.status_code != 200:
            #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

    else:
        form = CourtOrderForm()
    return render(request, 'documents/court_order_form.html', {'form': form})
