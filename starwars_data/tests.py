from django.test import TestCase
from django.urls import reverse

from starwars_data.models import Collection


class HomePageViewTestCase(TestCase):
    def test_homepage_view(self):
        """
        Tests that the homepage view returns a status code of 200 and uses the correct template
        """
        Collection.objects.create(file_name="file_name.csv")

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "starwars_data/collection_list.html")
