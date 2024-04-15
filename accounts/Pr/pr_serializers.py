import re

from django.contrib.auth.hashers import make_password
from django.conf.global_settings import EMAIL_HOST
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Professor, UserRole
from course.models import Course
from faculty.models import Faculty, Major

from faculty.serializers import FacultyGetDataSerializer, MajorGetDataSerializer
from term.Tr.tr_serializers import TermGetDataSerializer
from term.models import Term

class ProfessorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    professor_number = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    national_code = serializers.CharField()
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all())
    expertise = serializers.CharField()
    degree = serializers.CharField()
    past_teaching_lessons = serializers.ListField(required=False)

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
        if Professor.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("This email exist")
        if Professor.objects.filter(national_code=validated_data['national_code']).exists():
            raise ValidationError('This national code exist')
        user_data = {
            'role': 2,
            'username': f"pr_{validated_data['national_code']}",
            'password': make_password(validated_data['national_code']),
            'email': validated_data['email'],
        }
        create_role = UserRole.objects.create(**user_data)

        professor_data = {
            'professor': create_role,
            'professor_number': f"pr_{validated_data['national_code']}",
            'password': make_password(validated_data['national_code']),
            **validated_data
        }
        past_teaching_lessons = professor_data.pop('past_teaching_lessons', [])
        professor = Professor.objects.create(**professor_data)

        for lesson_id in past_teaching_lessons:
            if not Course.objects.filter(id=lesson_id).exists():
                raise serializers.ValidationError("This lesson does not exist")
        professor.past_teaching_lessons.set(past_teaching_lessons)
        return professor

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.firstname = validated_data.data.get('firstname', instance.firstname)
        instance.lastname = validated_data.data.get('lastname', instance.lastname)
        instance.email = validated_data.data.get('email', instance.email)
        instance.national_code = validated_data.data.get('national_code', instance.national_code)
        instance.term_id = validated_data.data.get('term', instance.term)
        instance.faculty_id = validated_data.data.get('faculty', instance.faculty)
        instance.major_id = validated_data.data.get('major', instance.major)
        instance.expertise = validated_data.data.get('expertise', instance.firstname)
        instance.degree = validated_data.data.get('degree', instance.degree)

        email = validated_data.data.get('email', instance.email)
        if Professor.objects.exclude(id=instance.id).filter(email=email).exists():
            raise ValidationError("This email exist")
        national_code = validated_data.data.get('national_code', instance.national_code)
        if Professor.objects.exclude(id=instance.id).filter(national_code=national_code).exists():
            raise ValidationError("This national_code exist")
        past_teaching_lessons = validated_data.data.get('past_teaching_lessons', [])
        for lesson_id in past_teaching_lessons:
            if not Course.objects.filter(id=lesson_id).exists():
                raise ValidationError('This lesson does not exist')
        instance.past_teaching_lessons.set(past_teaching_lessons)
        instance.save()
        instance.professor.email = instance.email
        instance.professor.save()
        return instance


class ProfessorGetDataSerializer(serializers.ModelSerializer):
    term_detail = TermGetDataSerializer(source='term')
    faculty_detail = FacultyGetDataSerializer(source='faculty')
    major_detail = MajorGetDataSerializer(source='major')


    class Meta:
        model = Professor
        fields = (
            'firstname', 'lastname', 'professor_number', 'email', 'national_code', 'term_detail', 'faculty_detail', 'major_detail',
            'expertise', 'degree', 'past_teaching_lessons',)


class ProfessorGetFullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('firstname', 'lastname',)