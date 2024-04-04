from wsgiref.validate import validator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils import timezone

from django.db import transaction

from accounts.serializers import StudentGetDataSerializer
from faculty.models import Faculty
from .models import Course, Subject

from term.models import Term
from accounts.models import Professor
from faculty.serializers import FacultyGetDataSerializer


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
    term_end_time = attrs['term'].term_end_time

    if not exams_start_time <= exam_time <= term_end_time:
        raise ValidationError("Times should be: term.exams_start_time <= exam_time <= term.term_end_time")


class CourseSerializer(serializers.Serializer):
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    professor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())

    # class_id -> new table for class? #TODO
    class_id = serializers.IntegerField()

    day = serializers.IntegerField()
    time = serializers.TimeField()
    capacity = serializers.IntegerField()
    exam_time = serializers.DateTimeField()
    exam_class_id = serializers.IntegerField()

    # TODO
    def validate(self, attrs):
        # NOTE
        # validate_time(attrs)

        validate_professorFaculty_subject(attrs)

        # NOTE
        # validate_exam_time(attrs)

        return attrs

    # TODO
    @transaction.atomic
    def create(self, validated_data):
        # "only IT_Manager & related_EA can create a course -> in view?"

        return Course.objects.create(**validated_data)

    # TODO
    @transaction.atomic
    def update(self, instance, validated_data):
        # TODO
        # IMPORTANT
        return instance


class CourseGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class PrerequisiteSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ('prerequisite', )


class SubjectGetDataSerializer(serializers.ModelSerializer):
    faculty_detail = FacultyGetDataSerializer(source='provider_faculty')
    prerequisite_detail = PrerequisiteSubjectSerializer(many=True, read_only=True, source='prerequisite')

    class Meta:
        model = Subject
        fields = ['id', 'name', 'number_of_course', 'course_type', 'mandatory', 'faculty_detail',
                  'corequisite', 'prerequisite_detail']
