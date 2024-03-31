from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class TestEAviews(APITestCase):

    # TODO
    fixtures = ["data.json"]

    def test_list_EA(self):
        response = self.client.get(reverse("educationalAssistant"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_EA(self):
        EA_sample = {
            "educational_assistant": "6a5c1aca-5088-45c4-abbe-8bbdcd294bfd",
            "assistant": "0d4c318e-f6f3-4a25-994b-9d141038f5ec",
            "faculty": "66971b0d-c482-46cd-ab6f-73a45322685d",
        }
        response = self.client.post(reverse("educationalAssistant"), EA_sample)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_EA_by_wrongPK_should_return_HTTP400(self):
        pk = "b3a2b78f-6742-4f01-a2c9-63cf1df1d956"
        response = self.client.get(reverse("EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_EA_by_correctPK_should_return_HTTP200(self):
        pk = "425d2328-84fd-4bd3-be0a-12bd81999443"
        response = self.client.get(reverse("EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_EA_by_wrongPK_return_HTTP400(self):
        pk = "b3a2b78f-6742-4f01-a2c9-63cf1df1d956"
        response = self.client.delete(reverse("EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_EA_by_correctPK_return_HTTP200(self):
        pk = "425d2328-84fd-4bd3-be0a-12bd81999443"
        response = self.client.delete(reverse("EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
