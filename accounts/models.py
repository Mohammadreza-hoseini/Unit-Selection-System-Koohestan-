from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver


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
        return f"{self.username}"


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
    password = models.CharField(max_length=256, verbose_name='رمز عبور')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    national_code = models.CharField(max_length=11, unique=True, verbose_name='کد ملی')
    term = models.ForeignKey("term.Term", on_delete=models.CASCADE, related_name='professor_term',
                             verbose_name='ترم جاری')
    faculty = models.ForeignKey("faculty.Faculty", on_delete=models.CASCADE, related_name='professor_faculty',
                                verbose_name='انتخاب دانشکده')
    major = models.ForeignKey("faculty.Major", on_delete=models.CASCADE, related_name='professor_major',
                              verbose_name='رشته')
    expertise = models.CharField(max_length=256, verbose_name='تخصص')
    degree = models.CharField(max_length=256, verbose_name='مرتبه یا درجه')
    past_teaching_lessons = models.ManyToManyField("course.Course", verbose_name='دروس تدریس شده', null=True,
                                                   blank=True, related_name='professor_past_teaching_lessons')

    def __str__(self):
        return f"pr_{self.national_code}"


class Student(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.OneToOneField(UserRole, on_delete=models.CASCADE, related_name='student_user_role',
                                   verbose_name='نوع کاربر')
    firstname = models.CharField(max_length=256, verbose_name='نام')
    lastname = models.CharField(max_length=256, verbose_name='نام خانوادگی')
    student_number = models.CharField(max_length=256, unique=True, verbose_name='شماره دانشجویی')
    password = models.CharField(max_length=256, verbose_name='رمز عبور')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='تصویر پروفایل', null=True, blank=True)
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
    average = models.FloatField(verbose_name='معدل کل', null=True, blank=True)
    term = models.ForeignKey("term.Term", on_delete=models.CASCADE, related_name='student_term',
                             verbose_name='ترم جاری')
    faculty = models.ForeignKey("faculty.Faculty", on_delete=models.CASCADE, related_name='student_faculty',
                                verbose_name='انتخاب دانشکده')
    major = models.ForeignKey("faculty.Major", on_delete=models.CASCADE, related_name='student_major',
                              verbose_name='انتخاب رشته تحصیلی')
    passed_lessons = models.ManyToManyField("course.Subject", verbose_name='دروس پاس شده', null=True, blank=True,
                                            related_name='student_passed_lessons')
    lessons_in_progress = models.ManyToManyField("course.Subject", verbose_name='دروس در حال گذراندن', null=True,
                                                 blank=True, related_name='student_lessons_in_progress')
    supervisor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='student_supervisor',
                                   verbose_name='انتخاب استاد راهنما')
    military_service_status = models.PositiveSmallIntegerField(choices=ChooseMilitaryServiceStatus.choices,
                                                               verbose_name='وضعیت نظام وظیفه')
    years = models.IntegerField(default=1, verbose_name='سنوات')

    def __str__(self):
        return f"st_{self.national_code}"


@receiver(post_save, sender=Student)
def add_student_term_average_record(sender, instance, **kwargs):
    create_std_term_avg = StudentTermAverage()
    create_std_term_avg.term_id = instance.term.id
    create_std_term_avg.student_id = instance.id
    create_std_term_avg.term_number += 1
    create_std_term_avg.save()


class ITManager(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    IT_manager = models.OneToOneField(UserRole, on_delete=models.CASCADE, related_name='ITManager_user_role',
                                      verbose_name='نوع کاربر')
    firstname = models.CharField(max_length=256, verbose_name='نام')
    lastname = models.CharField(max_length=256, verbose_name='نام خانوادگی')
    it_manager_number = models.CharField(max_length=256, unique=True, verbose_name='شماره منیجر آیتی')
    password = models.CharField(max_length=256, verbose_name='رمز عبور')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    national_code = models.CharField(max_length=11, unique=True, verbose_name='کد ملی')

    def __str__(self):
        return f"IT_{self.national_code}"


class EducationalAssistant(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    assistant = models.OneToOneField(Professor, on_delete=models.CASCADE, related_name='EducationalAssistant_assistant',
                                     verbose_name='آیدی استاد')
    faculty = models.OneToOneField("faculty.Faculty", on_delete=models.CASCADE,
                                   related_name='educational_assistant_faculty', verbose_name='انتخاب دانشکده')

    def __str__(self):
        return f"EA_{self.assistant.national_code}"


class University(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    address = models.TextField(verbose_name='آدرس دانشگاه')
    phone = models.CharField(verbose_name='شماره تماس')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    educational_assistant = models.OneToOneField(Professor, on_delete=models.CASCADE,
                                                 related_name='university_educational_assistant',
                                                 verbose_name='معاون آموزشی دانشگاه', null=True, blank=True)
    university_president = models.ForeignKey(Professor, on_delete=models.CASCADE,
                                             related_name='university_university_president',
                                             verbose_name='رئیس دانشگاه', null=True, blank=True)

    class Meta:
        unique_together = ('educational_assistant', 'university_president',)

    def __str__(self):
        return f"Uni_{self.phone}"


class OTPCode(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=6, verbose_name='کد یکبار مصرف')
    email = models.EmailField(verbose_name='ایمیل')
    code_expire = models.DateTimeField(blank=True, null=True, verbose_name='زمان منقضی شدن کد یکبار مصرف')

    def __str__(self):
        return f"{self.email} - {self.code} - {self.code_expire}"


class StudentTermAverage(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE,
                                related_name='student_term_average_student', verbose_name='دانشجو', null=True,
                                blank=True)
    term = models.ForeignKey("term.Term", on_delete=models.CASCADE, related_name='student_term_average_term',
                             verbose_name='ترم')
    average = models.FloatField(verbose_name='معدل ترم', null=True, blank=True)
    term_number = models.PositiveIntegerField(default=0, verbose_name='شماره ترم')

    def __str__(self):
        return f"{self.term.name} - {self.average}"
