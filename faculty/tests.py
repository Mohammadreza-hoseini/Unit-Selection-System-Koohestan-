import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Faculty


class FacultyAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_faculty(self):
        data = {
            'name': 'beheshti',
            'phone': '+989123456789',
            'address': '123 Main St',
            'university': 1
        }
        response = self.client.post(reverse('faculty-create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_phone(self):
        data = {
            'name': 'shariati',
            'phone': '12345',
            'address': '123 Main St',
            'university': 1
        }
        response = self.client.post(reverse('faculty-create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_faculty(self):
        response = self.client.get(reverse('get-all-faculty'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_faculty(self):
        faculty = Faculty.objects.create(name='besaat', phone='+989123456789', address='123 Test St',
                                         university_id=1)
        data = {
            'name': 'allame',
            'phone': '+989987654321',
            'address': '456 Updated St',
            'university': 2
        }
        response = self.client.put(reverse('faculty-update', kwargs={'pk': faculty.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_faculty(self):
        faculty = Faculty.objects.create(name='besaat', phone='+989123456789', address='123 Test St',
                                         university_id=1)
        response = self.client.get(reverse('faculty-detail', kwargs={'pk': faculty.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_faculty(self):
        faculty = Faculty.objects.create(name='besaat', phone='+989123456789', address='123 Test St',
                                         university_id=1)
        response = self.client.delete(reverse('faculty-delete', kwargs={'pk': faculty.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nonexistent_faculty_detail(self):
        response = self.client.get(reverse('faculty-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incomplete_data_create_faculty(self):
        data = {
            'name': 'beheshti'
        }
        response = self.client.post(reverse('faculty-create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()