from django.db import models
import uuid


class Term(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=256, verbose_name='نام ترم')
    # students = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name='term_students',
    #                              verbose_name='دانشجوها', null=True, blank=True)
    # professors = models.ForeignKey("accounts.Professor", on_delete=models.CASCADE, related_name='term_professor',
    #                                verbose_name='اساتید')
    # course_lists = models.ManyToManyField("course.Course", verbose_name='لیست دروس ترمی',
    #                                       related_name='term_course_lists', null=True, blank=True)
    start_selection_time = models.DateTimeField(verbose_name='زمان شروع انتخاب واحد')
    end_selection_time = models.DateTimeField(verbose_name='زمان پایان انتخاب واحد')
    class_start_time = models.DateTimeField(verbose_name='زمان شروع کلاس ها')
    class_end_time = models.DateTimeField(verbose_name='زمان پایان کلاس ها')
    doped_added_start_time = models.DateTimeField(verbose_name='زمان شروع حذف و اضافه')
    doped_added_end_time = models.DateTimeField(verbose_name='زمان پایان حذف و اضافه')
    emergency_removal_end_time = models.DateTimeField(verbose_name='زمان پایان حذف اضطراری')
    exam_start_time = models.DateTimeField(verbose_name='زمان شروع امتحانات')
    term_end_time = models.DateTimeField(verbose_name='زمان اتمام ترم')
    year = models.DateField(auto_now_add=True, verbose_name='سال جاری')

    def __str__(self):
        return f"{self.name}"


class ChooseRequestState(models.IntegerChoices):
    pending = 1, "pending"
    accepted = 2, "accepted"
    rejected = 3, "rejected"


class UnitRegisterRequest(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE,
                                related_name='unit_register_request_student', verbose_name='دانشجو')
    course = models.ManyToManyField("course.Course", related_name='unit_register_request_course', verbose_name='دروس')
    request_state = models.PositiveSmallIntegerField(
        default=ChooseRequestState.pending, choices=ChooseRequestState.choices, verbose_name='وضعیت درخواست'
    )

    def __str__(self):
        return f"req: {self.student.national_code} - {self.request_state}"


class BusyStudyingRequest(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE,
                                related_name='busy_studying_request_student', verbose_name='دانشجو')
    assistant = models.ForeignKey("accounts.EducationalAssistant", on_delete=models.CASCADE,
                                  related_name='busy_studying_request_assistant', verbose_name='معاون آموزشی')

    request_state = models.PositiveSmallIntegerField(
        default=ChooseRequestState.pending, choices=ChooseRequestState.choices, verbose_name='وضعیت درخواست'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"st_{self.student.student_number} - ea_{self.assistant.assistant.professor_number}"
