from django.db import transaction
from rest_framework import serializers

from accounts.models import Student, EducationalAssistant
from faculty.models import Faculty
from term.models import BusyStudyingRequest


class BusyStudyingRequestSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    def validate_student(self, value):
        get_student = Student.objects.filter(id=value).first()
        if get_student.gender != 1:
            raise serializers.ValidationError("Only males can make requests.")
        return get_student

    @transaction.atomic
    def create(self, validated_data):
        get_student = Student.objects.filter(id=validated_data.data['student']).first()
        get_faculty = Faculty.objects.filter(faculty=get_student.faculty).first()
        get_assistant = EducationalAssistant.objects.filter(faculty=get_faculty.name).first()
        print(get_assistant)
        validated_data.data['assistant'] = get_assistant.assistant
        busystudyingrequest = BusyStudyingRequest.objects.create(**validated_data)
        return busystudyingrequest

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.student = validated_data.data.get('student', instance.student)
        get_faculty = Faculty.objects.filter(faculty=validated_data.data['faculty']).first()
        get_assistant = EducationalAssistant.objects.filter(faculty=get_faculty.name).first()

        instance.assistant = validated_data.data['assistant'] = get_assistant.assistant

        instance.save()
        return instance


class busystudyingrequestGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusyStudyingRequest
        fields = '__all__'
