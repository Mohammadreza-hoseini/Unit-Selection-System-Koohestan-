from rest_framework import serializers
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.db import transaction

from koohestan.tasks import accept_emergency_removal_request, reject_emergency_removal_request
from term.models import EmergencyRemoval


class StudentEmergencyRemovalSerializer(serializers.Serializer):
    @transaction.atomic
    def create(self, validated_data):
        get_data = self.context['get_student_unit_request']
        get_course_id = self.context['course_id']
        if timezone.now() > get_data.term.emergency_removal_end_time:
            raise ValidationError('Emergency delete time has expired')
        if EmergencyRemoval.objects.filter(student=get_data.student, term=get_data.term,
                                           course=get_data.course.get(id=get_course_id)).exists():
            raise ValidationError('An application has been registered for this course')
        add_emergency_removal_request = EmergencyRemoval.objects. \
            create(student=get_data.student,
                   course=get_data.course.get(id=get_course_id),
                   term=get_data.term,
                   assistant=get_data.student.faculty.educational_assistant_faculty)
        return add_emergency_removal_request


class AssistantEmergencyRemovalSerializer(serializers.Serializer):
    request_state = serializers.ChoiceField(choices=[1, 2, 3])
    reason_rejected = serializers.CharField(required=False)

    @transaction.atomic
    def create(self, validated_data):
        get_data = self.context['get_emergency_removal_request']
        if validated_data['request_state'] == 2:
            get_data.request_state = validated_data['request_state']
            get_data.save()
            accept_emergency_removal_request(get_data.student.email)
        elif validated_data['request_state'] == 3:
            if 'reason_rejected' not in self.data:
                raise ValidationError('please enter reason rejected')
            get_data.request_state = validated_data['request_state']
            get_data.reason_rejected = self.data['reason_rejected']
            get_data.save()
            reject_emergency_removal_request(get_data.student.email, validated_data['reason_rejected'])
        return get_data


class StudentGetDataEmergencyRemovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRemoval
        fields = '__all__'
