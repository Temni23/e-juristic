from django.urls import path

from .views import *

app_name = "documents"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("download/", DownloadView.as_view(), name="download"),
    path('test/', resume_pdf, name='court_order_create_test'),
]


