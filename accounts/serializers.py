import random
import re
from django.contrib.auth.hashers import make_password
from django.conf.global_settings import EMAIL_HOST
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from course.models import Course
from faculty.models import Faculty, Major
from .models import Student, Professor, UserRole


def validate_phone(value):
    pattern = '^(\+98|0)?9\d{9}$'
    result = re.match(pattern, value)
    if not result:
        raise ValidationError("phone number format is wrong")
    elif Student.objects.filter(phone=value).first():
        raise ValidationError("This phone exist")


def validate_email(value):
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    result = bool(pattern.match(value))
    if result is False:
        raise ValidationError("email format is wrong")
    elif Student.objects.filter(email=value).first():
        raise ValidationError("This email exist")


def validate_national_code(value):
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


def validate_faculty(value):
    check_faculty_exist = Faculty.objects.filter(id=value).first()
    if not check_faculty_exist:
        raise ValidationError('This faculty does not exist')


def validate_major(value):
    check_major_exist = Major.objects.filter(id=value).first()
    if not check_major_exist:
        raise ValidationError('This major does not exist')


def validate_supervisor(value):
    check_supervisor_exist = Professor.objects.filter(id=value).first()
    if not check_supervisor_exist:
        raise ValidationError('This professor does not exist')


class StudentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    student_number = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    email = serializers.EmailField(validators=[validate_email])
    phone = serializers.CharField(validators=[validate_phone])
    national_code = serializers.CharField(validators=[validate_national_code])
    gender = serializers.ChoiceField(choices=[1, 2])
    birth_date = serializers.DateField()
    entry_year = serializers.DateField()
    incoming_semester = serializers.ChoiceField(choices=[1, 2], default=1)
    average = serializers.FloatField(read_only=True)
    faculty = serializers.UUIDField(validators=[validate_faculty])
    major = serializers.UUIDField(validators=[validate_major])
    passed_lessons = serializers.ListField(required=False)
    lessons_in_progress = serializers.ListField()
    supervisor = serializers.UUIDField(validators=[validate_supervisor])
    military_service_status = serializers.ChoiceField(choices=[1, 2, 3])
    years = serializers.IntegerField(default=1, required=False)

    def create(self, validated_data):
        create_role = UserRole.objects.create(role=1)
        create_student = Student()
        create_student.student = create_role
        create_student.firstname = validated_data['firstname']
        create_student.lastname = validated_data['lastname']
        create_student.student_number = f"st_{validated_data['national_code']}"
        create_student.password = make_password(validated_data['national_code'])
        create_student.email = validated_data['email']
        create_student.phone = validated_data['phone']
        create_student.national_code = validated_data['national_code']
        create_student.gender = validated_data['gender']
        create_student.birth_date = validated_data['birth_date']
        create_student.entry_year = validated_data['entry_year']
        create_student.incoming_semester = validated_data['incoming_semester']
        create_student.faculty_id = validated_data['faculty']
        create_student.major_id = validated_data['major']
        create_student.supervisor_id = validated_data['supervisor']
        create_student.military_service_status = validated_data['military_service_status']
        create_student.years = validated_data['years']
        create_student.save()
        for item in validated_data['lessons_in_progress']:
            check_lessons_exist = Course.objects.filter(id=item).first()
            if not check_lessons_exist:
                raise ValidationError('This lesson is not exist')
            create_student.lessons_in_progress.add(check_lessons_exist)
            create_student.save()
        return create_student

    def update(self, instance, validated_data):
        ...
#         add update student


class StudentGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
        'id', 'firstname', 'lastname', 'student_number', 'email', 'phone', 'national_code', 'gender', 'birth_date',
        'entry_year', 'incoming_semester', 'average',)
