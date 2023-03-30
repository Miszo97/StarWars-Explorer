from django.urls import path

from starwars_data.views import (
    CollectionDetailView,
    CollectionView,
    GenerateCollectionView,
)

urlpatterns = [
    path("api/generate", GenerateCollectionView.as_view(), name="generate"),
    path("api/collections/<int:pk>", CollectionDetailView.as_view(), name="collection-detail"),
    path("api/collections", CollectionView.as_view(), name="collection"),
]
