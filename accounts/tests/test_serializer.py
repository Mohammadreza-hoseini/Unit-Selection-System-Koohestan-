from django.test import TestCase

from ..serializers import EducationalAssistantSerializer


class AssistantSerializerTest(TestCase):

    # change corresponding to data.json file TODO: 
    fixtures = ["data.json"]

    def test_invalid_assistant(self):
        data = {
            "assistant": "b3a2b78f-6742-4f01-a2c9-63cf1df1d956",
            "faculty": "0cba684b-58c9-4727-8a17-c51efbd847be",
        }
        serializer = EducationalAssistantSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("assistant", serializer.errors)

    def test_valid_assistant(self):
        data = {
            "assistant": "61e407a4-6ff3-4ad8-aee3-07e06b69bab1",
            "faculty": "0cba684b-58c9-4727-8a17-c51efbd847be",
        }
        serializer = EducationalAssistantSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_faculty(self):
        data = {
            "assistant": "61e407a4-6ff3-4ad8-aee3-07e06b69bab1",
            "faculty": "ecb3b155-459f-4ce2-959a-13a52bca1b65",
        }
        serializer = EducationalAssistantSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("faculty", serializer.errors)

    def test_valid_faculty(self):
        data = {
            "assistant": "61e407a4-6ff3-4ad8-aee3-07e06b69bab1",
            "faculty": "0cba684b-58c9-4727-8a17-c51efbd847be",
        }
        serializer = EducationalAssistantSerializer(data=data)
        self.assertTrue(serializer.is_valid())
