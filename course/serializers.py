from wsgiref.validate import validator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from django.utils import timezone

from django.db import transaction

from .models import Course, Subject

from term.models import Term
from accounts.models import Professor




# validations:
    # 1) 'professor.faculty' matches 'subject.provider_faculty' #DONE
    # 2) class with 'class_id' should be empty in that 'day' and 'time' #DONE
    # 3) 'exam_time' should be between 'term.exam_start_time' and 'term.exam_end_time' #DONE 
    # 4) class with 'exam_class_id' should be empty in that 'exam_time'
    # 5) optional: classModel.capacity >= course.capacity

def validate_time(attrs):
    # Validation 1
            # Check if the doped_added_end_time has passed or not
    term_doped_added_end_time = attrs['term'].doped_added_end_time
    current_datetime = timezone.now()
    if current_datetime >= term_doped_added_end_time:
        raise ValidationError("term_doped_added_end_time has passed")


def validate_professorFaculty_subject(attrs):
    # Validation 2
                # Check if professor.faculty matches subject.provider_faculty
    prof_faculty = attrs['professor'].faculty.id
    subject_provider_faculty = attrs['subject'].provider_faculty.id
    if prof_faculty != subject_provider_faculty:
        raise ValidationError("Professor_faculty and subject_provider_faculty don't match")

def validate_exam_time(attrs):
    exam_time = attrs['exam_time']
    exams_start_time = attrs['term'].exam_start_time
    exams_end_time = attrs['term'].exam_end_time

    if not exams_start_time <= exam_time <= exams_end_time:
        raise ValidationError("Times should be: term.exams_start_time <= exam_time <= term.exams_end_time")

class CourseSerializer(serializers.Serializer):
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    professor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())
    # class_id -> new table for class? #TODO
    
    day = serializers.IntegerField()
    time = serializers.TimeField()
    capacity = serializers.IntegerField()
    exam_time = serializers.DateTimeField()
    exam_class_id = serializers.IntegerField()
    
    
    
    #TODO
    def validate(self, attrs):
        
        validate_time(attrs)
        
        validate_professorFaculty_subject(attrs)
        
        validate_exam_time(attrs)
        
        
        return attrs
    
    #TODO
    @transaction.atomic
    def create(self, validated_data):
        # "only IT_Manager & related_EA can create a course -> in view?"
        
        return Term.objects.create(**validated_data)
    
    #TODO
    @transaction.atomic
    def update(self, instance, validated_data):
        ...
        
        return instance
    
class CourseGetDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = "__all__"