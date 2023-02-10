from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("documents.urls", namespace="documents")),
    path('admin/', admin.site.urls),
]
