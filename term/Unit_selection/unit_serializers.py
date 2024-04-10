from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from course.models import Course
from course.serializers import CourseGetDataSerializer
from term.models import Term, UnitRegisterRequest

from .unit_validations import validate_passed_course, validate_student_add_unit_average, \
    validate_exam_and_class_time_interference, validate_courses_related_to_the_field, \
    \
    validate_prerequisite_subject_passed, validate_course_capacity, validate_checking_student_years, validate_Student_URForm_Term, \
    UR_update_delete, validate_St_current_term_UR, validate_UR_selection_time
        


class URFormSerializer(serializers.Serializer):
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    course = serializers.ListField()

    def validate(self, attrs):

        student_obj = self.context.get('student_obj')

        validate_UR_selection_time(attrs)
        validate_St_current_term_UR(attrs, student_obj)
        validate_passed_course(attrs, student_obj)
        validate_course_capacity(attrs)
        
        # TODO possible
            # if Math1 should be deleted then its corequisite courses(Math2) should be deleted too #TODO
                # otherwise raise ValidationError(corequisite subject cannot be deleted before the main subject)  
        validate_prerequisite_subject_passed(attrs, student_obj)
        
        validate_student_add_unit_average(attrs, student_obj)
        validate_exam_and_class_time_interference(attrs)
        validate_courses_related_to_the_field(attrs, student_obj)
        validate_checking_student_years(attrs, student_obj)



        return attrs

    @transaction.atomic
    def create(self, validated_data):

        courses = validated_data['course']
        term_id = validated_data['term'].id

        # retrieve additional_data in self.context
        student_obj = self.context.get('student_obj')
        
        #check if term.id = course.term.id #TODO 
        try:
            term_obj = Term.objects.get(id=term_id)
        except:
            raise serializers.ValidationError('This term does not exist')    
                
        already_exist_form = validate_Student_URForm_Term(term_id, student_obj.id)
        
        # create new UnitRegisterRequest   
        UR_form_obj = UnitRegisterRequest(student=student_obj, term=term_obj)

        check_repetitive_course = []

        for course in courses:
            if course in check_repetitive_course:
                raise serializers.ValidationError(f'{course} Repetitive course')
            check_repetitive_course.append(course)
            if not Course.objects.filter(id=course).exists():
                raise serializers.ValidationError("This course does not exist")

        # set M2M field
        UR_form_obj.course.set(courses)

        
        
        if already_exist_form is not None:
            # add 1 capacity to already_exist_form.courses + delete already_exist_form
            
            UR_update_delete(already_exist_form)
            already_exist_form.delete()
            
        
        UR_form_obj.save()
        return UR_form_obj


class URFormGetDataSerializer(serializers.ModelSerializer):
    term = serializers.PrimaryKeyRelatedField(queryset = Term.objects.all())
    UR_courses = CourseGetDataSerializer(many=True, source='course')
    request_state = serializers.IntegerField()

    class Meta:
        model = UnitRegisterRequest
        fields = ("term", "UR_courses", 'request_state')
