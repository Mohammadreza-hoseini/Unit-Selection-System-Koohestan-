from django.db import transaction

from django.http import QueryDict
from rest_framework import serializers


from accounts.models import Student
import course
from term.models import Term, UnitRegisterRequest

from course.serializers import CourseGetDataSerializer

class UR_Form_Serializer(serializers.Serializer):
    course = serializers.ListField()
    

    def validate(self, attrs):
        
        # validations
        # #TODO

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        
        courses = validated_data['course']
        
        # retrieve additional_data in self.context
        student_obj = self.context.get('student_obj')
        
        UR_form_obj = UnitRegisterRequest(student=student_obj)        
        
        # set M2M field
        UR_form_obj.course.set(courses)
        UR_form_obj.save()
        
        return UR_form_obj
    

    @transaction.atomic
    def update(self, instance, validated_data):
        
        ...


class UR_Form_GetDataSerializer(serializers.ModelSerializer):
    
    # student = serializers
    
    course = serializers.ListField()
    
    
    class Meta:
        model = UnitRegisterRequest
        fields = "__all__"


