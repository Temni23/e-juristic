from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, FormView
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.shortcuts import render
from django.views.generic import FormView
from xhtml2pdf.files import pisaFileObject

from .forms import CourtOrderForm
from django.http import FileResponse, response
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas

def generate_pdf(request):
    if request.method == 'POST':
        form = CourtOrderForm(request.POST)
        if form.is_valid():
            # debtor_surname = form.cleaned_data['debtor_surname']
            # debtor_name = form.cleaned_data['debtor_name']
            # debtor_lastname = form.cleaned_data['debtor_lastname']
            # court_number = form.cleaned_data['court_number']
            # court_city = form.cleaned_data['court_city']
            # debtor_adres = form.cleaned_data['debtor_adres']
            # court_order_date = form.cleaned_data['court_order_date']
            # court_order_number = form.cleaned_data['court_order_number']
            # claimer_name = form.cleaned_data['claimer_name']
            # debt_size = form.cleaned_data['debt_size']
            # court_order_date_receipt = form.cleaned_data['court_order_date_receipt']

            # x2pdf creae func

            template_path = 'court_order/create.html'
            context = form.cleaned_data
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            # для скачивания раскомментируй стороку снизу
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # отображение файла в браузере без скачивания
            response['Content-Disposition'] = 'filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response, encoding='UTF-8', link_callback=link_callback)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

            # buffer = BytesIO()
            # pdf = canvas.Canvas(buffer)
            #
            # # Add your PDF generation logic here
            # pdf.setFont("Helvetica", 12)
            # pdf.drawString(100, 750, "Фамилия заявителя: {}".format(debtor_surname))
            # pdf.drawString(100, 700, "Имя заявителя: {}".format(debtor_name))
            # pdf.drawString(100, 650, "Отчество заявителя: {}".format(debtor_lastname))
            # pdf.drawString(100, 600, "Номер судебного участка: {}".format(court_number))
            # pdf.drawString(100, 550, "Город: {}".format(court_city))
            # pdf.drawString(100, 500, "Адрес заявителя: {}".format(debtor_adres))
            # pdf.drawString(100, 450, "Дата вынесения судебного приказа: {}".format(court_order_date))
            # pdf.drawString(100, 400, "Номер судебного приказа: {}".format(court_order_number))
            # pdf.drawString(100, 350, "Имя заявителя: {}".format(claimer_name))
            #
            # pdf.save()
            # buffer.seek(0)
            # return FileResponse(buffer, as_attachment=True, filename='court_order.pdf')
    else:
        form = CourtOrderForm()
    return render(request, 'court_order_form.html', {'form': form})


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


class HomeView(TemplateView):
    template_name = "documents/home.html"

class CourtOrderView(FormView):
    form_class = CourtOrderForm
    template_name = "documents/courtorder.html"
    success_url = reverse_lazy('documents:download')

class DownloadView(TemplateView):
    template_name = "documents/download.html"