from rest_framework import serializers
from .models import Faculty, Major


class FacultyGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class MajorGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'
