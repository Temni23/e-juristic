from django.urls import path

from .views import *

app_name = "documents"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("courtorder/", CourtOrderView.as_view(), name="courtorder"),
    path("download/", DownloadView.as_view(), name="download"),
    path('create/', generate_pdf, name='court_order_create'),
]
