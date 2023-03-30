from starwars_data.models import Collection
from rest_framework.test import APIClient
import pytest


pytestmark = pytest.mark.django_db

class TestCollectionsView:
    def test_get_collections(self):
        Collection.objects.create(file_name = "abc")
        client = APIClient()
        response = client.get('/api/collections')
        assert response.status_code == 200
        assert len(response.data) == 1


class TestGenerateView:
    def test_post_generate(self):
        client = APIClient()
        response = client.post('/api/generate')
        assert response.status_code == 200

