from django.contrib import admin
from django.urls import path

from starwars_data.views import craete_dataset

urlpatterns = [path("admin/", admin.site.urls), path("generate/", craete_dataset)]
