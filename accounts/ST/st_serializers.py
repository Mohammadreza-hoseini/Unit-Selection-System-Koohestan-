from rest_framework import serializers

from accounts import queryset
from accounts.models import Student
from course.models import Subject
from course.serializers import SubjectGetDataSerializer

class ST_Passed_Courses_GET(serializers.ModelSerializer):
    ...
    passed_lessons = SubjectGetDataSerializer(many=True, source='passed_lessons')
    class Meta:
        model = Student
        fields = ("passed_lessons", )