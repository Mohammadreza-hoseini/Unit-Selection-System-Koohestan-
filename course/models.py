from django.db import models
import uuid

from accounts.models import Professor, Student
from faculty.models import Faculty
from term.models import Term


class ChooseCourseType(models.IntegerChoices):
    basic = 1, "basic"
    specialized = 2, "specialized"
    general = 3, "general"


class Subject(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=256)
    provider_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='subject_faculty',
                                         verbose_name='دانشکده ارائه دهنده')
    prerequisite = models.ManyToManyField('self', verbose_name='دروس پیش نیاز')
    corequisite = models.ManyToManyField('self', verbose_name='دروس همنیاز')
    number_of_course = models.PositiveIntegerField(verbose_name='تعداد واحد درس')
    course_type = models.PositiveSmallIntegerField(
        default=ChooseCourseType.basic, choices=ChooseCourseType.choices, verbose_name="نوع درس"
    )
    mandatory = models.IntegerField(default=1, verbose_name='وضعیت اجباری بودن یا نبودن درس')

    def __str__(self):
        return self.name


class ChooseDayOfWeek(models.IntegerChoices):
    saturday = 1, "saturday"
    sunday = 2, "sunday"
    monday = 3, "monday"
    tuesday = 4, "tuesday"
    wednesday = 5, "wednesday"
    thursday = 6, "thursday"
    friday = 7, "friday"


class Course(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_subject',
                                verbose_name='درس مصوب')
    class_id = models.PositiveIntegerField(verbose_name='شماره کلاس', unique=True)
    day = models.PositiveSmallIntegerField(
        default=ChooseDayOfWeek.saturday, choices=ChooseDayOfWeek.choices, verbose_name="انتخاب روز"
    )
    time = models.TimeField(verbose_name='زمان کلاس')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='course_professor',
                                  verbose_name='استاد')
    capacity = models.PositiveIntegerField(verbose_name='ظرفیت')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='course_term', verbose_name='ترم')
    exam_time = models.DateTimeField(verbose_name='تاریخ و زمان امتحان')
    exam_class_id = models.PositiveIntegerField(verbose_name='شماره کلاس امتحان')

    def __str__(self):
        return f"{self.class_id}"
