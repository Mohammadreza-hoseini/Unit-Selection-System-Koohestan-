from django.test import TestCase

from ..serializers import EducationalAssistantSerializer


class AssistantSerializerTest(TestCase):

    fixtures = ["data.json"]

    def test_valid_data(self):
        data = ...
        serializer = EducationalAssistantSerializer(data, many=True)
        self.assertTrue(serializer.is_valid)
        self.assertEqual(serializer.validated_data, data)

    def test_invalid_data(self): ...
