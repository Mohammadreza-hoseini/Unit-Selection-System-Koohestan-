from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from faculty.models import Faculty
from accounts.models import Professor, EducationalAssistant

from accounts.Pr.pr_serializers import ProfessorGetDataSerializer, ProfessorGetFullNameSerializer


class EducationalAssistantSerializer(serializers.Serializer):
    assistant = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())

    @transaction.atomic
    def create(self, validated_data):

        # DRY principle #TODO
        A_id = validated_data["assistant"]
        faculty_id = validated_data["faculty"]

        prof_obj = Professor.objects.filter(pk=A_id).first()
        faculty_obj = Faculty.objects.filter(pk=faculty_id).first()

        user_obj = prof_obj.professor

        if user_obj.role == 4:
            raise ValidationError("User is already an educational_assistant")

        if user_obj.role != 2:
            raise ValidationError("User isn't a professor")

        if prof_obj.faculty_id != str(faculty_id):
            raise ValidationError("Professor and Faculty don't match")

        user_obj.role = 4
        user_obj.save()

        EA_object = EducationalAssistant.objects.create(
            assistant=prof_obj, faculty=faculty_obj
        )

        return EA_object

    @transaction.atomic
    def update(self, instance, validated_data):

        # NOTE//////////////////////
        # TODO

        A_id = validated_data.data.get("assistant", instance.assistant)
        faculty_id = validated_data.data.get("faculty", instance.faculty)

        # if the professor changes and faculty remains the same
        if A_id != instance.assistant:
            new_EA_candidate = Professor.objects.get(pk=A_id)

            if new_EA_candidate.faculty.id != faculty_id:
                raise ValidationError("Professor and Faculty don't match")

            # change role of previous EA to 'professor'
            user_of_preEA = instance.assistant.professor
            user_of_preEA.role = 2
            user_of_preEA.save()

            # delete the previous EA
            instance.delete()

            data_for_newEA = {'assistant': A_id, "faculty": faculty_id}

            return data_for_newEA

        # the professor remains the same but faculty changes
        else:

            raise ValidationError('Assistant_id should be different.')


class EA_GetDataSerializer(serializers.ModelSerializer):
    professor_detail = ProfessorGetDataSerializer(source='assistant')

    class Meta:
        model = EducationalAssistant
        fields = ('id', 'professor_detail')


class EA_GetFullNameSerializer(serializers.ModelSerializer):
    Professor_detail = ProfessorGetFullNameSerializer(source='assistant')

    class Meta:
        model = EducationalAssistant
        fields = ('Professor_detail',)