import random
import re
from django.conf.global_settings import EMAIL_HOST
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from .models import Student


class StudentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    student_number = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    national_code = serializers.CharField(required=True)
    gender = serializers.ChoiceField(required=True, choices=['male', 'female'])
    birth_date = serializers.DateField(required=True)
    entry_year = serializers.DateField(required=True)
    incoming_semester = serializers.ChoiceField(choices=['first', 'second'], default='first')
    average = serializers.FloatField(read_only=True)
    faculty = serializers.UUIDField(required=True)
    major = serializers.UUIDField(required=True)
    passed_lessons = serializers.CharField(required=False)
    lessons_in_progress = serializers.CharField(required=True)
    supervisor = serializers.UUIDField(required=True)
    military_service_status = serializers.ChoiceField(choices=['permanentExemption', 'educationPardon', 'inductee'])
    years = serializers.IntegerField(default=1, required=False)

    def validate_phone(self, value):
        pattern = '^(\+98|0)?9\d{9}$'
        result = re.match(pattern, value)
        if not result:
            raise ValidationError("phone number format is wrong")
        elif Student.objects.filter(phone=value).first():
            raise ValidationError("This phone exist")
        return value

    def validate_email(self, value):
        pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        result = bool(pattern.match(value))
        if result is False:
            raise ValidationError("email format is wrong")
        elif Student.objects.filter(email=value).first():
            raise ValidationError("This email exist")
        return value

    def validate_national_code(self, value):
        val_str = str(value)
        if len(str(val_str)) != 10:
            raise ValidationError('national code is 10 digits')
        s = sum([int(val_str[i]) * (10 - i) for i in range(9)])
        d, m = divmod(s, 11)
        if m < 2:
            if int(val_str[-1]) != m:
                raise ValidationError('invalid national code')
        else:
            if int(val_str[-1]) != 11 - m:
                raise ValidationError('invalid national code')

    def create(self, validated_data):
        print(validated_data)
