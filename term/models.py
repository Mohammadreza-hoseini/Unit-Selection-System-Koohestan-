from django.db import models
import uuid

from accounts.models import Student, Professor
from course.models import Course


class Term(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=256, verbose_name='نام ترم')
    students = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='term_students',
                                 verbose_name='دانشجوها')
    professors = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='term_professor',
                                   verbose_name='اساتید')
    course_lists = models.ManyToManyField(Course, verbose_name='لیست دروس ترمی')
    start_selection_time = models.DateTimeField(verbose_name='زمان شروع انتخاب واحد')
    end_selection_time = models.DateTimeField(verbose_name='زمان پایان انتخاب واحد')
    class_start_time = models.DateTimeField(verbose_name='زمان شروع کلاس ها')
    class_end_time = models.DateTimeField(verbose_name='زمان پایان کلاس ها')
    repair_start_time = models.DateTimeField(verbose_name='زمان شروع ترمیم')
    repair_end_time = models.DateTimeField(verbose_name='زمان پایان ترمیم')
    emergency_removal_end_time = models.DateTimeField(verbose_name='زمان پایان حذف اضطراری')
    exam_start_time = models.DateTimeField(verbose_name='زمان شروع امتحانات')
    term_end_time = models.DateTimeField(verbose_name='زمان اتمام ترم')

    def __str__(self):
        return f"{self.name}"
