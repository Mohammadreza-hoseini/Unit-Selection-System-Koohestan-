import re
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from accounts.models import University
from .models import Faculty, Major


class FacultySerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    def validate_phone(self, value):
        pattern = '^(\+98|0)?9\d{9}$'
        result = re.match(pattern, value)
        if not result:
            raise ValidationError("phone number format is wrong")
        return value

    @transaction.atomic
    def create(self, validated_data):
        if Faculty.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("This name exist")
        if Faculty.objects.filter(phone=validated_data['phone']).exists():
            raise serializers.ValidationError("This phone exist")

        faculty = Faculty.objects.create(**validated_data)
        return faculty

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.data.get('name', instance.name)
        instance.phone = validated_data.data.get('phone', instance.phone)
        instance.address = validated_data.data.get('address', instance.address)
        instance.university.id = validated_data.data.get('university', instance.university)

        phone = validated_data.data.get('phone', instance.phone)
        if Faculty.objects.exclude(id=instance.id).filter(phone=phone).exists():
            raise serializers.ValidationError('this phone exist')

        name = validated_data.data.get('name', instance.name)
        if Faculty.objects.exclude(id=instance.id).filter(name=name).exists():
            raise serializers.ValidationError('this name exist')

        instance.save()
        return instance


class UniversityGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"


class FacultyGetDataSerializer(serializers.ModelSerializer):
    university_detail = UniversityGetDataSerializer(source='university')

    class Meta:
        model = Faculty
        fields = ('id', 'name', 'phone', 'address', 'university_detail')


class MajorGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'
