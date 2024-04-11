from accounts.models import Student
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from course.models import Course
from term.models import UnitRegisterRequest



def validate_students_id(attrs, course_obj, term_obj):
    """
        1) validate student id
        2) check if the student has this course
    """
    
    
    students = attrs['students']
    for student_id in students:
        
        
        try:
            get_student = Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            raise ValidationError(f'{student_id} student does not exist')
        
        if get_student.term.id != term_obj.id:
            raise ValidationError('Term and Student do not match')
        
        student_has_course = UnitRegisterRequest.objects.filter(student__id=student_id, course__id=course_obj.id, request_state=2,
                                                                term__id=term_obj.id).exists()
        if not student_has_course:
            raise ValidationError(f'{student_id} student does not have this course')

def validate_prof_course_match(prof_obj, course_obj):
    if course_obj.professor.id != prof_obj.id:
        raise ValidationError('Prof and Course do not match')
    
    
def validate_term_match(course_obj, prof_obj, attrs):
    term_obj = attrs['term']
    if course_obj.term.id != term_obj.id:
        raise ValidationError('Term and Course do not match')
    if prof_obj.term.id != term_obj.id:
        raise ValidationError('Term and Prof do not match')
    
def validate_time(term_obj):
    if not timezone.now() < term_obj.term_end_time:
        raise ValidationError('Cannot add score after term_end_time')
    
def validate_scores(scores):
    for score in scores:
        if not 0 <= score <= 20:
            raise ValidationError("Rule: 0 <= Score <= 20")