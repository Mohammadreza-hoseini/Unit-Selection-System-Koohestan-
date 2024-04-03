from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class TestEAviews(APITestCase):

    # create new dumpdata in data.json #TODO
    fixtures = ["data.json"]
    

    def test_list_EA(self):
        response = self.client.get(reverse("accounts:assistants_get_all"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_EA(self):
        EA_sample = {
            "assistant": "99c9a225-a9a8-448d-903d-119c61f619ac",
            "faculty": "0cba684b-58c9-4727-8a17-c51efbd847be"
        }
        response = self.client.post(reverse("accounts:educationalAssistant"), EA_sample)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_EA_by_wrongPK_should_return_HTTP400(self):
        pk = "0cba684b-58c9-4727-8a17-c51efbd847be"
        response = self.client.get(reverse("accounts:EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_EA_by_correctPK_should_return_HTTP200(self):
        pk = "ed1c658b-13ed-4f62-87e7-dd15b5bc040f"
        response = self.client.get(reverse("accounts:EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_EA_by_wrongPK_return_HTTP400(self):
        pk = "0cba684b-58c9-4727-8a17-c51efbd847be"
        response = self.client.delete(reverse("accounts:EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_EA_by_correctPK_return_HTTP200(self):
        pk = "ed1c658b-13ed-4f62-87e7-dd15b5bc040f"
        response = self.client.delete(reverse("accounts:EA_withPK", args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
