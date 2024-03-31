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
from django.db import transaction
from course.models import Course
from faculty.models import Faculty, Major
from .models import Student, Professor, UserRole, EducationalAssistant


class StudentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    student_number = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    phone = serializers.CharField()
    national_code = serializers.CharField()
    gender = serializers.ChoiceField(choices=[1, 2])
    birth_date = serializers.DateField()
    entry_year = serializers.DateField()
    incoming_semester = serializers.ChoiceField(choices=[1, 2], default=1)
    average = serializers.FloatField(read_only=True)
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all())
    passed_lessons = serializers.ListField(required=False)
    lessons_in_progress = serializers.ListField()
    supervisor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())
    military_service_status = serializers.ChoiceField(choices=[1, 2, 3])
    years = serializers.IntegerField(default=1, required=False)

    def validate_phone(self, value):
        pattern = '^(\+98|0)?9\d{9}$'
        result = re.match(pattern, value)
        if not result:
            raise serializers.ValidationError("phone number format is wrong")
        return value

    def validate_email(self, value):
        pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not pattern.match(value):
            raise serializers.ValidationError("email format is wrong")
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
        return value

    @transaction.atomic
    def create(self, validated_data):
        if Student.objects.filter(phone=validated_data['phone']).exists():
            raise serializers.ValidationError("This phone exist")
        if Student.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("This email exist")
        if Student.objects.filter(national_code=validated_data['national_code']).exists():
            raise ValidationError('This national code exist')
        user_data = {
            'role': 1,
            'username': f"st_{validated_data['national_code']}",
            'password': make_password(validated_data['national_code']),
        }
        create_role = UserRole.objects.create(**user_data)

        student_data = {
            'student': create_role,
            'student_number': f"st_{validated_data['national_code']}",
            'password': make_password(validated_data['national_code']),
            **validated_data
        }
        lessons_in_progress = student_data.pop('lessons_in_progress', [])
        student = Student.objects.create(**student_data)

        for lesson_id in lessons_in_progress:
            if not Course.objects.filter(id=lesson_id).exists():
                raise serializers.ValidationError("This lesson does not exist")
        student.lessons_in_progress.set(lessons_in_progress)
        return student

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.firstname = validated_data.data.get('firstname', instance.firstname)
        instance.lastname = validated_data.data.get('lastname', instance.lastname)
        instance.email = validated_data.data.get('email', instance.email)
        instance.phone = validated_data.data.get('phone', instance.phone)
        instance.national_code = validated_data.data.get('national_code', instance.national_code)
        instance.gender = validated_data.data.get('gender', instance.gender)
        instance.birth_date = validated_data.data.get('birth_date', instance.birth_date)
        instance.entry_year = validated_data.data.get('entry_year', instance.entry_year)
        instance.incoming_semester = validated_data.data.get('incoming_semester', instance.incoming_semester)
        instance.average = validated_data.data.get('average', instance.average)
        instance.faculty_id = validated_data.data.get('faculty', instance.faculty)  # Assign Faculty instance directly
        instance.major_id = validated_data.data.get('major', instance.major)  # Assign Faculty instance directly
        instance.supervisor_id = validated_data.data.get('supervisor',
                                                         instance.supervisor)  # Assign Faculty instance directly
        instance.military_service_status = validated_data.data.get('military_service_status',
                                                                   instance.military_service_status)
        instance.years = validated_data.data.get('years', instance.years)

        # Check email uniqueness, excluding the current student being updated
        email = validated_data.data.get('email', instance.email)
        if Student.objects.exclude(id=instance.id).filter(email=email).exists():
            raise ValidationError("This email exist")
        phone = validated_data.data.get('phone', instance.phone)
        if Student.objects.exclude(id=instance.id).filter(phone=phone).exists():
            raise ValidationError('This phone exist')
        national_code = validated_data.data.get('national_code', instance.national_code)
        if Student.objects.exclude(id=instance.id).filter(national_code=national_code).exists():
            raise ValidationError('This national_code exist')
        lessons_in_progress = validated_data.data.get('lessons_in_progress', [])
        for lesson_id in lessons_in_progress:
            if not Course.objects.filter(id=lesson_id).exists():
                raise ValidationError("This lesson does not exist")

        instance.lessons_in_progress.set(lessons_in_progress)
        instance.save()
        return instance


class StudentGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id', 'firstname', 'lastname', 'student_number', 'email', 'phone', 'national_code', 'gender', 'birth_date',
            'entry_year', 'incoming_semester', 'average',)


def validate_educational_assistant(value):
    user_obj = UserRole.objects.filter(pk=value).first()
    if not user_obj:
        raise ValidationError("User doesn't exist")


def validate_assistant(value):
    prof_obj = Professor.objects.filter(pk=value).first()
    if not prof_obj:
        raise ValidationError("Professor doesn't exist")


def validate_faculty(value):
    faculty_obj = Faculty.objects.filter(pk=value).first()
    if not faculty_obj:
        raise ValidationError("Faculty doesn't exist")


class EducationalAssistantSerializer(serializers.Serializer):
    educational_assistant = serializers.UUIDField(validators=[validate_educational_assistant], required=True)
    assistant = serializers.UUIDField(validators=[validate_assistant], required=True)
    faculty = serializers.UUIDField(validators=[validate_faculty], required=True)

    # TODO
    # which fields to show (for example name, ....)

    def create(self, validated_data):

        # DRY principle #TODO
        user_id = validated_data["educational_assistant"]
        A_id = validated_data["assistant"]
        faculty_id = validated_data["faculty"]

        user_obj = UserRole.objects.filter(pk=user_id).first()
        prof_obj = Professor.objects.filter(pk=A_id).first()
        faculty_obj = Faculty.objects.filter(pk=faculty_id).first()

        if user_obj.role == 4:
            raise ValidationError("User is already an educational_assistant")

        if user_obj.role != 2:
            raise ValidationError("User isn't a professor")

        if prof_obj.faculty_id != str(faculty_id):
            raise ValidationError("Professor and Faculty don't match")

        user_obj.role = 4
        user_obj.save()

        EA_object = EducationalAssistant.objects.create(
            educational_assistant=user_obj, assistant=prof_obj, faculty=faculty_obj
        )

        return EA_object

    def update(self, instance, validated_data):
        # make scenario -> what can be updated exactly? #QUESTION

        # DRY principle #TODO
        user_id = validated_data["educational_assistant"]
        A_id = validated_data["assistant"]
        faculty_id = validated_data["faculty"]

        user_obj = UserRole.objects.filter(pk=user_id).first()
        prof_obj = Professor.objects.filter(pk=A_id).first()
        faculty_obj = Faculty.objects.filter(pk=faculty_id).first()

        if user_obj.role != 4:
            raise ValidationError("User is not an educational_assistant")

        # other validations ... #TODO

        # update ... #TODO
