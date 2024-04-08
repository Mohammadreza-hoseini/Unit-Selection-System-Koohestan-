from rest_framework.exceptions import ValidationError
from accounts.models import StudentTermAverage
from course.models import Course
from django.db.models import F


def validate_passed_course(attrs, student_obj):
    passed_lessons = student_obj.passed_lessons
    course = attrs["course"]

    for course_id in course:

        # TEST it
        # possible #BUG
        if course_id in passed_lessons:
            raise ("This course has already been passed")

    print(passed_lessons)


def validate_course_capacity(attrs):
    course = attrs["course"]

    for course_id in course:
        course_obj = Course.objects.filter(id=course_id)
        if course_obj.capacity <= 0:
            raise ("No more capacity for this course")


def validate_student_add_unit_average(attrs, student_obj):
    course = attrs["course"]
    get_student = StudentTermAverage.objects.filter(student=student_obj)
    max_units_selection = 0
    if get_student.exists():
        get_student_average = get_student.order_by(F('id').desc()).last()
        if get_student_average.average >= 17:
            max_units_selection = 24
        elif get_student_average.average < 17:
            max_units_selection = 20
    elif not get_student.exists():
        max_units_selection = 20
    sum_units_selection = 0
    for item in course:
        get_course = Course.objects.filter(id=item).first()
        if not get_course:
            raise ValidationError('This Course id is not exist')
        sum_units_selection += get_course.subject.number_of_course
    if sum_units_selection > max_units_selection:
        raise ValidationError('The number of your course units is more than the allowed limit')
