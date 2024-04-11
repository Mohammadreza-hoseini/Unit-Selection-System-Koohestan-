from django.db import transaction
from django.utils import timezone
from rest_framework import serializers


from accounts.models import Student
from course.models import ScoreTable
        
from .ApReq_validations import validate_courses_id, validate_students_id, validate_student_has_course

class ScoreTableSerializer(serializers.Serializer):
    students = serializers.ListField()
    scores = serializers.ListField()


    def validate(self, attrs):
        
        validate_students_id(attrs)
        validate_courses_id(attrs)
        validate_student_has_course(attrs)
        


        return attrs

    @transaction.atomic
    def create(self, validated_data):
        ...
        

