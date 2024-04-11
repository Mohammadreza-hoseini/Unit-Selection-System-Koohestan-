from accounts.models import Student
from rest_framework.exceptions import ValidationError

from course.models import Course



def validate_students_id(attrs):
    students = attrs['students']
    for student_id in students:
        student_exist = Student.objects.filter(id=student_id).exists()
        if not student_exist:
            raise ValidationError(f'{student_id} student does not exist')

def validate_courses_id(attrs):
    courses = attrs['courses']
    for course_id in courses:
        course_exist = Course.objects.filter(id=course_id).exists()
        if not course_exist:
            raise ValidationError(f'{course_id} course does not exist')