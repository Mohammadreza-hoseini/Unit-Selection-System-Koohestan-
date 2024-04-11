from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db import transaction

from term.models import Term

from accounts.models import Student, Professor


def validate_times(attrs):
    true_order = (attrs['start_selection_time'] < attrs['end_selection_time']
                  < attrs['class_start_time'] < attrs['doped_added_start_time']
                  < attrs['doped_added_end_time'] < attrs['emergency_removal_end_time']
                  < attrs['class_end_time'] < attrs['exam_start_time']
                  < attrs['term_end_time'])
    if not true_order:
        raise ValidationError("""Order of times should be: \
                            start_selection_time <  end_selection_time < class_start_time < doped_added_start_time < doped_added_end_time < emergency_removal_end_time < class_end_time < exam_start_time < term_end_time)""")


class TermSerializer(serializers.Serializer):
    name = serializers.CharField()
    start_selection_time = serializers.DateTimeField()
    end_selection_time = serializers.DateTimeField()
    class_start_time = serializers.DateTimeField()
    class_end_time = serializers.DateTimeField()
    doped_added_start_time = serializers.DateTimeField()
    doped_added_end_time = serializers.DateTimeField()
    emergency_removal_end_time = serializers.DateTimeField()
    exam_start_time = serializers.DateTimeField()
    term_end_time = serializers.DateTimeField()

    def validate(self, attrs):
        """
        Object-level validation
        """
        validate_times(attrs)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        return Term.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.data.get('name', instance.name)

        # IMPORTANT
        # add other fields too #TODO

        if Term.objects.exclude(id=instance.id).filter(name=instance.name).exists():
            raise ValidationError("There is already a term with this name")
        instance.save()
        return instance


class TermGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = "__all__"
