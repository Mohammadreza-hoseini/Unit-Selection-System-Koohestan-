import random
import re
from django.contrib.auth.hashers import make_password
from django.utils import timezone
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
from accounts import queryset
from course.models import Course
from faculty.models import Faculty, Major
from faculty.serializers import FacultyGetDataSerializer, MajorGetDataSerializer
from koohestan.tasks import send_email_task
from term.models import Term
from term.serializers import TermGetDataSerializer
from .models import Professor, UserRole, EducationalAssistant, OTPCode


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def _generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def _generate_expire_time(self):
        return timezone.now() + timezone.timedelta(seconds=60)

    def validate(self, attrs):
        email = attrs['email']
        if not UserRole.objects.filter(email=email).exists():
            raise ValidationError('User does not exist')

        code = self._generate_otp()
        expire_time = self._generate_expire_time()
        OTPCode.objects.create(code=code, email=email, code_expire=expire_time)

        # send email
        send_email_task.delay(email, code)
        return attrs


class ChangePasswordAction(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        code = attrs['code']
        get_otp_code = OTPCode.objects.filter(code=code)
        if not get_otp_code.exists():
            raise ValidationError('This code does not exist')
        elif timezone.now() > get_otp_code.first().code_expire:
            raise ValidationError('The code has expired')
        elif code != get_otp_code.first().code:
            raise ValidationError('Code is wrong')
        return attrs

    def create(self, validated_data):
        get_otp_code = OTPCode.objects.filter(code=validated_data['code']).first()
        get_user = UserRole.objects.get(email=get_otp_code.email)
        get_user.password = make_password(validated_data['password'])
        get_user.save()
        get_user.student_user_role.password = make_password(validated_data['password'])
        get_user.student_user_role.save()
        return get_user


# End code of Mohammadreza hoseini

class UserRoleGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id', 'username', 'role')


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
