from django.db import models
import uuid


class ChooseCourseType(models.IntegerChoices):
    basic = 1, "basic"
    specialized = 2, "specialized"
    general = 3, "general"
    practical = 4, "practical"


class ChooseMandatory(models.IntegerChoices):
    yes = 1, "yes"
    no = 2, "no"


class Subject(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=256)
    provider_faculty = models.ForeignKey("faculty.Faculty", on_delete=models.CASCADE,
                                         related_name='subject_faculty',
                                         verbose_name='دانشکده ارائه دهنده')
    prerequisite = models.ManyToManyField('self', symmetrical=False, verbose_name='دروس پیش نیاز',
                                          related_name='subject_prerequisite',
                                          null=True, blank=True)
    corequisite = models.ManyToManyField('self', symmetrical=False, verbose_name='دروس همنیاز',
                                         related_name='subject_corequisite',
                                         null=True, blank=True)
    number_of_course = models.PositiveIntegerField(verbose_name='تعداد واحد درس')
    course_type = models.PositiveSmallIntegerField(
        default=ChooseCourseType.basic, choices=ChooseCourseType.choices, verbose_name="نوع درس"
    )
    mandatory = models.PositiveSmallIntegerField(
        default=ChooseMandatory.yes, choices=ChooseMandatory.choices, verbose_name='وضعیت اجباری بودن یا نبودن درس'
    )

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
    professor = models.ForeignKey("accounts.Professor", on_delete=models.CASCADE, related_name='course_professor',
                                  verbose_name='استاد')
    capacity = models.PositiveIntegerField(verbose_name='ظرفیت')
    term = models.ForeignKey("term.Term", on_delete=models.CASCADE, related_name='course_term', verbose_name='ترم جاری')
    exam_time = models.DateTimeField(verbose_name='تاریخ و زمان امتحان')
    exam_class_id = models.PositiveIntegerField(verbose_name='شماره کلاس امتحان')

    def __str__(self):
        return f"{self.class_id}"


class ChooseCoursePassStatus(models.IntegerChoices):
    passed = 1, 'passed'
    failed = -1, 'failed'
    pending = 0, 'pending'


class ChooseReconsiderationStatus(models.IntegerChoices):
    no_ApReq = 0, 'no appeal request'
    rejected = -1, 'rejected'
    accepted = 1, 'accepted'
    pending = 2, 'pending'


class ScoreTable(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='student_score',
                                verbose_name='دانشجو')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='score_course',
                               verbose_name='درس ترمی')
    score = models.IntegerField(verbose_name='نمره', default=-1)  # -1 -> no score
    course_pass_status = models.IntegerField(default=ChooseCoursePassStatus.pending,
                                             choices=ChooseCoursePassStatus.choices,
                                             verbose_name='وضعیت قبولی درس ترمی')
    score_finalized_status = models.BooleanField(default=False)
    reconsideration_status = models.IntegerField(default=ChooseReconsiderationStatus.no_ApReq,
                                                 choices=ChooseReconsiderationStatus.choices,
                                                 verbose_name='وضعیت درخواست تجدید نظر')
