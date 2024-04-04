from wsgiref.validate import validator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils import timezone

from django.db import transaction

from faculty.models import Faculty
from .models import Course, Subject

from term.models import Term
from accounts.models import Professor

# Start code of Mohammadreza hoseini
class SubjectSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    provider_faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    prerequisite = serializers.ListField(required=False)
    corequisite = serializers.ListField(required=False)
    number_of_course = serializers.IntegerField()
    course_type = serializers.ChoiceField(choices=[1, 2, 3], required=True)
    mandatory = serializers.ChoiceField(choices=[1, 2], required=True)

    @transaction.atomic
    def create(self, validated_data):
        if Subject.objects.filter(name=validated_data['name']).exists():
            raise ValidationError("This name exist")
        subject_data = {
            **validated_data
        }
        prerequisite = subject_data.pop('prerequisite', [])
        corequisite = subject_data.pop('corequisite', [])
        subject = Subject.objects.create(**subject_data)

        for lesson_prerequisite in prerequisite:
            if not Subject.objects.filter(id=lesson_prerequisite).exists():
                raise ValidationError("This subject does not exist")
        subject.prerequisite.set(prerequisite)
        for lesson_corequisite in corequisite:
            if not Subject.objects.filter(id=lesson_corequisite).exists():
                raise ValidationError("This subject does not exist")
        subject.corequisite.set(corequisite)
        return subject
# End code of Mohammadreza hoseini

#------- Start code Arman Shakerian ----------

# validations:
# 1) 'professor.faculty' matches 'subject.provider_faculty' #DONE
# 2) class with 'class_id' should be empty in that 'day' and 'time' 
# 3) 'exam_time' should be between 'term.exam_start_time' and 'term.exam_end_time' #DONE
# 4) class with 'exam_class_id' should be empty in that 'exam_time' #DONE

def validate_time(attrs):
    """
        Validation 1
        Check if the doped_added_end_time has passed or not
    """
    term_doped_added_end_time = attrs['term'].doped_added_end_time
    current_datetime = timezone.now()
    if current_datetime >= term_doped_added_end_time:
        raise ValidationError("term_doped_added_end_time has passed")


def validate_professorFaculty_subject(attrs):
    """
        Validation 2
        Check if professor.faculty matches subject.provider_faculty
    """
    prof_faculty = attrs['professor'].faculty.id
    subject_provider_faculty = attrs['subject'].provider_faculty.id
    if prof_faculty != subject_provider_faculty:
        raise ValidationError("Professor_faculty and subject_provider_faculty don't match")
    
    
def validate_exam_time(attrs):
    """
        Validation 3
        -) Check if term.exams_start_time <= exam_time <= term.term_end_time
        -) no exam for practical subjects
    """
    
    course_type = attrs['subject'].course_type
    
    if course_type == 4: #practical subject
        return "practical"
    elif "exam_time" not in attrs:
        raise ValidationError("Exam_time is required")
    
    exam_time = attrs['exam_time']
    exams_start_time = attrs['term'].exam_start_time
    term_end_time = attrs['term'].term_end_time

    if not exams_start_time <= exam_time <= term_end_time:
        raise ValidationError("Times should be: term.exams_start_time <= exam_time <= term.term_end_time")
    

def validate_class_id(attrs):
    """
        Validation 4
        -) check intervening course time
    """
    class_id = attrs['class_id']
    day_of_class = attrs['day']
    time_of_class = attrs['time']
    
    intervening_class = Course.objects.filter(class_id= class_id, day=day_of_class, time=time_of_class).exists()
    if intervening_class:
        raise ValidationError("There is already a course with the same 'day' & 'time' in class with this 'class_id'")

def validate_exam_class_id(attrs):
    """
        Validation 5
        -) check intervening exam time
    """
    exam_time = attrs['exam_time']
    exam_class_id = attrs['exam_class_id']
    intervening_exam = Course.objects.filter(exam_time=exam_time, exam_class_id=exam_class_id).exists()
    if intervening_exam:
        raise ValidationError("There is already an exam with the same 'exam_time' in class with this 'class_id'")
            


def validate_professor_term(attrs):
    """
        Validation 6
        -) course.professor.term & course.term must match
    """
    course_term = attrs['term'].id
    prof_term = attrs['professor'].term.id
    if course_term != prof_term:
        raise ValidationError('Professor is not for this Term')


class CourseSerializer(serializers.Serializer):
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    professor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())

    
    class_id = serializers.IntegerField()

    day = serializers.IntegerField()
    time = serializers.TimeField()
    capacity = serializers.IntegerField()
    exam_time = serializers.DateTimeField(required=False)
    exam_class_id = serializers.IntegerField()


    def validate(self, attrs):
        
        validate_time(attrs)
        
        validate_professor_term(attrs)

        validate_professorFaculty_subject(attrs)

        subject_type = validate_exam_time(attrs)
        if subject_type is not None and subject_type == 'practical':
            # NOTE
            # default exam_time for practical subjects (which don't have exam)
            attrs['exam_time'] = "1111-11-11 11:11:11.000000 +00:00"


        return attrs

    @transaction.atomic
    def create(self, validated_data):
        
        validate_class_id(validated_data)
        
        validate_exam_class_id(validated_data)
        
        return Course.objects.create(**validated_data)
    
    

    @transaction.atomic
    def update(self, instance, validated_data):
        
        instance.subject = validated_data.data.get('subject', instance.subject)
        instance.class_id = validated_data.data.get('class_id', instance.class_id)
        instance.day = validated_data.data.get('day', instance.day)
        instance.time = validated_data.data.get('time', instance.time)
        instance.professor = validated_data.data.get('professor', instance.professor)
        instance.capacity = validated_data.data.get('capacity', instance.capacity)
        instance.term = validated_data.data.get('term', instance.term)
        instance.exam_time = validated_data.data.get('exam_time', instance.exam_time)
        instance.exam_class_time = validated_data.data.get('exam_class_time', instance.exam_class_time)
        
        intervening_class = Course.objects.exclude(instance).filter(class_id=instance.class_id, day=instance.day, time=instance.time).exists()
        if intervening_class:
            raise ValidationError("There is already a course with the same 'day' & 'time' in class with this 'class_id'")
        
        intervening_exam = Course.objects.filter(exam_time=instance.exam_time, exam_class_id=instance.exam_class_id).exists()
        if intervening_exam:
            raise ValidationError("There is already an exam with the same 'exam_time' in class with this 'class_id'")
            
            
        instance.save()
        
        return instance


class CourseGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

#------- End code Arman Shakerian ----------
