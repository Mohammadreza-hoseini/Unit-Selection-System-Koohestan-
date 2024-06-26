import re

from django.contrib.auth.hashers import make_password
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from term.models import Term
from faculty.models import Faculty, Major
from course.models import Course
from accounts.models import UserRole, Professor, Student

from accounts.models import Student
from course.models import Subject
from course.serializers import SubjectGetDataSerializer


class ST_Passed_Courses_Serializer(serializers.ModelSerializer):
    """
    Student's passed courses
    """
    ...
    passed_lessons = SubjectGetDataSerializer(many=True, source='passed_lessons')

    class Meta:
        model = Student
        fields = ("passed_lessons",)


class ST_Progress_Courses_Serializer(serializers.ModelSerializer):
    lessons_in_progress = SubjectGetDataSerializer(many=True)

    class Meta:
        model = Student
        fields = ("lessons_in_progress",)
        # fields = '__all__'


# Start code of Mohammadreza hoseini
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
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all())
    passed_lessons = serializers.ListField(required=False)
    lessons_in_progress = serializers.ListField(required=True)
    supervisor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())
    military_service_status = serializers.ChoiceField(choices=[1, 2, 3])
    years = serializers.IntegerField(default=1, required=False)
    avatar = serializers.ImageField(required=False)

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
            'email': validated_data['email'],
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
            if not Subject.objects.filter(id=lesson_id).exists():
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
        instance.term_id = validated_data.data.get('term', instance.term)
        instance.faculty_id = validated_data.data.get('faculty', instance.faculty)  # Assign Faculty instance directly
        instance.major_id = validated_data.data.get('major', instance.major)  # Assign Faculty instance directly
        instance.supervisor_id = validated_data.data.get('supervisor',
                                                         instance.supervisor)  # Assign Faculty instance directly
        instance.military_service_status = validated_data.data.get('military_service_status',
                                                                   instance.military_service_status)
        instance.years = validated_data.data.get('years', instance.years)
        instance.avatar = self.initial_data['avatar']

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
            if not Subject.objects.filter(id=lesson_id).exists():
                raise ValidationError("This lesson does not exist")

        instance.lessons_in_progress.set(lessons_in_progress)
        instance.save()
        instance.student.email = instance.email
        instance.student.save()
        return instance


class StudentGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id', 'firstname', 'lastname', 'avatar', 'student_number', 'email', 'phone', 'national_code', 'gender',
            'birth_date',
            'entry_year', 'incoming_semester', 'average', 'term', 'faculty', 'major', 'passed_lessons',
            'lessons_in_progress',
            'supervisor', 'military_service_status', 'years',)
