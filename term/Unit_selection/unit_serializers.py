from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from course.models import Course
from course.serializers import CourseGetDataSerializer
from term.models import Term, UnitRegisterRequest

from .unit_validations import validate_passed_course, validate_student_add_unit_average, \
    validate_exam_and_class_time_interference, validate_courses_related_to_the_field, validate_prerequisite_subject_passed, validate_course_capacity


class URFormSerializer(serializers.Serializer):
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    course = serializers.ListField()

    def validate(self, attrs):

        student_obj = self.context.get('student_obj')

        validate_passed_course(attrs, student_obj)
        validate_course_capacity(attrs)
        validate_prerequisite_subject_passed(attrs, student_obj)
        validate_student_add_unit_average(attrs, student_obj)
        validate_exam_and_class_time_interference(attrs)
        validate_courses_related_to_the_field(attrs, student_obj)



        return attrs

    @transaction.atomic
    def create(self, validated_data):

        courses = validated_data['course']
        term_id = validated_data['term']

        # retrieve additional_data in self.context
        student_obj = self.context.get('student_obj')
        
        #check if term.id = course.term.id #TODO 
        try:
            term_obj = Term.objects.get(id=term_id.id)
        except:
            raise serializers.ValidationError('This term does not exist')    
                
        UR_form_obj = UnitRegisterRequest(student=student_obj, term=term_obj)

        for course in courses:
            if not Course.objects.filter(id=course).exists():
                raise serializers.ValidationError("This course does not exist")

        # set M2M field
        UR_form_obj.course.set(courses)

        UR_form_obj.save()

        return UR_form_obj

    @transaction.atomic
    def update(self, instance, validated_data):

        ...


class URFormGetDataSerializer(serializers.ModelSerializer):    
    UR_courses = CourseGetDataSerializer(many=True, source='course')
    request_state = serializers.IntegerField()

    class Meta:
        model = UnitRegisterRequest
        fields = ("UR_courses", 'request_state')
