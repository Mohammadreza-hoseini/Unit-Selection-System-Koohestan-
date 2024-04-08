from rest_framework.exceptions import ValidationError

from course.models import Course


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
