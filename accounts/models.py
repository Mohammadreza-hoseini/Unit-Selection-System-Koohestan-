from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from course.models import Course
from faculty.models import Faculty, Major


class ChooseUserRole(models.IntegerChoices):
    student = 1, "student"
    professor = 2, "professor"
    ITManager = 3, "ITManager"
    educationalAssistant = 4, "educationalAssistant"


class UserRole(AbstractUser):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    role = models.PositiveSmallIntegerField(
        default=ChooseUserRole.student, choices=ChooseUserRole.choices, verbose_name="سطح دسترسی"
    )

    def __str__(self):
        return str(self.role)


class ChooseGender(models.IntegerChoices):
    male = 1, "male"
    female = 2, "female"


class ChooseSemester(models.IntegerChoices):
    first = 1, "first"
    second = 2, "second"


class ChooseMilitaryServiceStatus(models.IntegerChoices):
    permanentExemption = 1, "permanentExemption"
    educationPardon = 2, "educationPardon"
    inductee = 3, "inductee"


class Professor(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    professor = models.OneToOneField(UserRole, on_delete=models.CASCADE, related_name='professor_user_role',
                                     verbose_name='نوع کاربر')
    firstname = models.CharField(max_length=256, verbose_name='نام')
    lastname = models.CharField(max_length=256, verbose_name='نام خانوادگی')
    professor_number = models.CharField(max_length=256, unique=True, verbose_name='شماره استادی')
    national_code = models.CharField(max_length=11, unique=True, verbose_name='کد ملی')
    faculty = models.ManyToManyField(Faculty, related_name='professor_faculty', verbose_name='انتخاب دانشکده')
    field = models.CharField(max_length=256, verbose_name='رشته')
    expertise = models.CharField(max_length=256, verbose_name='تخصص')
    degree = models.CharField(max_length=256, verbose_name='مرتبه یا درجه')
    past_teaching_lessons = models.ManyToManyField(Course, verbose_name='دروس تدریس شده')

    def __str__(self):
        return f"{self.national_code}"


class Student(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.OneToOneField(UserRole, on_delete=models.CASCADE, related_name='student_user_role',
                                   verbose_name='نوع کاربر')
    firstname = models.CharField(max_length=256, verbose_name='نام')
    lastname = models.CharField(max_length=256, verbose_name='نام خانوادگی')
    student_number = models.CharField(max_length=256, unique=True, verbose_name='شماره دانشجویی')
    password = models.CharField(max_length=256, verbose_name='رمز عبور')
    avatar = models.URLField(max_length=256, verbose_name='تصویر پروفایل')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    national_code = models.CharField(max_length=11, unique=True, verbose_name='کد ملی')
    gender = models.PositiveSmallIntegerField(
        default=ChooseGender.male, choices=ChooseGender.choices, verbose_name='جنسیت'
    )
    birth_date = models.DateField(verbose_name='تاریخ تولد')
    entry_year = models.DateField(verbose_name='سال ورودی')
    incoming_semester = models.PositiveSmallIntegerField(
        default=ChooseSemester.first, choices=ChooseSemester.choices, verbose_name='ترم ورودی'
    )
    average = models.FloatField(verbose_name='معدل')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='student_faculty',
                                verbose_name='انتخاب دانشکده')
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='student_major',
                              verbose_name='انتخاب رشته تحصیلی')
    passed_lessons = models.ManyToManyField(Course, verbose_name='دروس پاس شده')
    lessons_in_progress = models.ManyToManyField(Course, verbose_name='دروس در حال گذراندن')
    supervisor = models.OneToOneField(Professor, on_delete=models.CASCADE, related_name='student_supervisor',
                                      verbose_name='انتخاب استاد راهنما')
    military_service_status = models.PositiveSmallIntegerField(choices=ChooseGender.choices,
                                                               verbose_name='وضعیت نظام وظیفه')
    years = models.IntegerField(default=0, verbose_name='سنوات')

    def __str__(self):
        return f"{self.student_number}"


class ITManager(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    IT_manager = models.OneToOneField(UserRole, on_delete=models.CASCADE, related_name='ITManager_user_role',
                                      verbose_name='نوع کاربر')
    firstname = models.CharField(max_length=256, verbose_name='نام')
    lastname = models.CharField(max_length=256, verbose_name='نام خانوادگی')
    it_manager_number = models.CharField(max_length=256, unique=True, verbose_name='شماره منیجر آیتی')
    national_code = models.CharField(max_length=11, unique=True, verbose_name='کد ملی')

    def __str__(self):
        return f"{self.it_manager_number}"


class EducationalAssistant(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    educational_assistant = models.OneToOneField(UserRole, on_delete=models.CASCADE,
                                                 related_name='EducationalAssistant_user_role',
                                                 verbose_name='نوع کاربر')
    firstname = models.CharField(max_length=256, verbose_name='نام')
    lastname = models.CharField(max_length=256, verbose_name='نام خانوادگی')
    employee_number = models.CharField(max_length=256, unique=True, verbose_name='شماره کارمندی')
    national_code = models.CharField(max_length=11, unique=True, verbose_name='کد ملی')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='educational_assistant_faculty',
                                verbose_name='انتخاب دانشکده')
    major = models.OneToOneField(Major, on_delete=models.CASCADE, related_name='educational_assistant_major',
                                 verbose_name='انتخاب رشته تحصیلی')

    class Meta:
        unique_together = ('faculty', 'major',)

    def __str__(self):
        return f"{self.employee_number}"
