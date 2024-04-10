from django.db import transaction
from rest_framework import serializers

from accounts.EA.ea_serializers import EA_GetFullNameSerializer
from accounts.St.st_serializers import StudentGetDataSerializer
from accounts.models import Student, EducationalAssistant
from faculty.models import Faculty
from term.models import BusyStudyingRequest


class BusyStudyingRequestSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    def validate_student(self, value):
        if value.gender != 1:
            raise serializers.ValidationError("Only males can make requests.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        get_assistant = EducationalAssistant.objects.filter(faculty_id=validated_data['student'].faculty.id).first()
        busy_studying_request = BusyStudyingRequest.objects.create(student=validated_data['student'],
                                                                   assistant=get_assistant)
        return busy_studying_request

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.student = validated_data.data.get('student', instance.student)
        get_faculty = Faculty.objects.filter(faculty=validated_data.data['faculty']).first()
        get_assistant = EducationalAssistant.objects.filter(faculty=get_faculty.name).first()

        instance.assistant = validated_data.data['assistant'] = get_assistant.assistant

        instance.save()
        return instance


class BusyStudyingRequestGetDataSerializer(serializers.ModelSerializer):
    student_detail = StudentGetDataSerializer(source='student')
    assistant_detail = EA_GetFullNameSerializer(source='assistant')

    class Meta:
        model = BusyStudyingRequest
        fields = ('id', 'created_at', 'request_state', 'student_detail', 'assistant_detail')
