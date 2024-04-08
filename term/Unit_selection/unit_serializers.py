from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from course.models import Course
from term.models import UnitRegisterRequest

from .unit_validations import validate_passed_course


class URFormSerializer(serializers.Serializer):
    course = serializers.ListField()

    def validate(self, attrs):

        student_obj = self.context.get('student_obj')

        validate_passed_course(attrs, student_obj)

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        courses = validated_data['course']

        # retrieve additional_data in self.context
        student_obj = self.context.get('student_obj')

        UR_form_obj = UnitRegisterRequest(student=student_obj)

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
    # student = serializers

    course = serializers.ListField()

    class Meta:
        model = UnitRegisterRequest
        fields = "__all__"
