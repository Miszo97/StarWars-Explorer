from django.contrib import admin
from django.urls import path

from starwars_data.views import (AggregateData, ColectionView, GenerateCollectionView,
                                 HomePageView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("generate", GenerateCollectionView.as_view(), name="generate"),
    path("", HomePageView.as_view(), name="home"),
    path("collections/<int:pk>", ColectionView.as_view(), name="collections"),
    path("collections/<int:pk>/aggregate", AggregateData.as_view(), name="aggregate"),
]
