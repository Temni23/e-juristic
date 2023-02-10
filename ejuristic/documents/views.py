from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, FormView
from django.shortcuts import render

from .forms import CourtOrderForm


class HomeView(TemplateView):
    template_name = "documents/home.html"

class CourtOrderView(FormView):
    form_class = CourtOrderForm
    template_name = "documents/courtorder.html"
    success_url = reverse_lazy('documents:download')

class DownloadView(TemplateView):
    template_name = "documents/download.html"