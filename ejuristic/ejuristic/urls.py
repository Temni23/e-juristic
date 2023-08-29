from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("documents.urls", namespace="documents")),
    path('admin/', admin.site.urls),
]
