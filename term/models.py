from django.db import models
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import StudentTermAverage, Student


class Term(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=256, verbose_name='نام ترم', null=True, blank=True)
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


@receiver(post_save, sender=Term)
def student_term_number(sender, instance, **kwargs):
    get_all_students = Student.objects.all()
    for student in get_all_students:
        get_student_on_term_average = StudentTermAverage.objects.filter(student=student).first()
        create_student_term_average = StudentTermAverage()
        create_student_term_average.term_id = instance.id
        create_student_term_average.student = get_student_on_term_average.student
        create_student_term_average.term_number = get_student_on_term_average.term_number + 1
        create_student_term_average.save()


class ChooseRequestState(models.IntegerChoices):
    pending = 1, "pending"
    accepted = 2, "accepted"
    rejected = 3, "rejected"


class UnitRegisterRequest(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE,
                                related_name='unit_register_request_student', verbose_name='دانشجو')
    course = models.ManyToManyField("course.Course", related_name='unit_register_request_course', verbose_name='دروس')
    supervisor = models.ForeignKey("accounts.Professor", on_delete=models.CASCADE,
                                   related_name='unit_register_request_supervisor',
                                   verbose_name='استاد راهنما', null=True, blank=True)
    request_state = models.PositiveSmallIntegerField(
        default=ChooseRequestState.pending, choices=ChooseRequestState.choices, verbose_name='وضعیت درخواست'
    )
    term = models.ForeignKey("term.Term", on_delete=models.CASCADE, related_name='unit_request_term',
                             verbose_name='ترم ')

    def __str__(self):
        return f"req: {self.student.national_code} - Term: {self.term} - Status: {self.request_state}"


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

@receiver(post_save, sender=UnitRegisterRequest)
def reduce_course_capacity(sender, instance, created, **kwargs):
    courses = instance.course.all()

    for course in courses:
        course.capacity -= 1
        course.save()