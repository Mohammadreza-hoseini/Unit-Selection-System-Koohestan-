from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Student, Professor
from course.models import Course
from course.serializers import CourseGetDataSerializer
from koohestan.tasks import sending_weekly_schedule
from term.models import Term, UnitRegisterRequest

from .unit_validations import validate_passed_course, validate_student_add_unit_average, \
    validate_exam_and_class_time_interference, validate_courses_related_to_the_field, \
    validate_prerequisite_subject_passed, validate_course_capacity, validate_checking_student_years


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
        validate_checking_student_years(attrs, student_obj)

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        courses = validated_data['course']
        term_id = validated_data['term']

        # retrieve additional_data in self.context
        student_obj = self.context.get('student_obj')

        # check if term.id = course.term.id #TODO
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
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    UR_courses = CourseGetDataSerializer(many=True, source='course')
    request_state = serializers.IntegerField()

    class Meta:
        model = UnitRegisterRequest
        fields = ("term", "UR_courses", 'request_state')


class SendFormSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    def validate(self, attrs):
        get_student = UnitRegisterRequest.objects.filter(student_id=attrs['student']).first()
        if timezone.now() > get_student.term.end_selection_time:
            raise ValidationError('The unit selection time has expired and you cannot submit the form')
        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        get_student = UnitRegisterRequest.objects.filter(student=validated_data['student']).first()
        get_student.supervisor_id = get_student.student.supervisor_id
        get_student.save()
        return get_student


class AcceptOrRejectFormSerializer(serializers.Serializer):
    supervisor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())
    request_state = serializers.ChoiceField(choices=[1, 2, 3])

    def validate(self, attrs):
        student_obj = self.context.get('student_obj')
        form_obj = self.context.get('get_form')
        query_check_form_exist = UnitRegisterRequest.objects.filter(id=form_obj.id, student=student_obj,
                                                                    supervisor=attrs['supervisor']).first()
        if not query_check_form_exist:
            raise ValidationError('This form does not exist')
        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        get_form = self.context['get_form']
        UnitRegisterRequest.objects.filter(id=get_form.id).update(request_state=validated_data['request_state'])
        if validated_data['request_state'] == 2:
            sending_weekly_schedule(self.context['student_obj'], get_form)
        return get_form
