from rest_framework.exceptions import ValidationError

from django.core.exceptions import ObjectDoesNotExist

from course.models import ScoreTable
from term.models import UnitRegisterRequest

def validate_term(student_obj, course_obj, term_obj):
    if student_obj.term.id != term_obj.id:
        return ValidationError('Student and term do not match')
    if course_obj.term.id != term_obj.id:
        return ValidationError('Course and term do not match')
        


def validate_student_has_course(student_obj, course_obj, term_obj):
    student_has_course = UnitRegisterRequest.objects.filter(student__id=student_obj.id, course__id=course_obj.id, request_state=2,
                                                                term__id=term_obj.id).exists()
    if not student_has_course:
        return ValidationError('Student does not have this course')

def validate_score_and_ApReq_state(student_obj, course_obj):
    try:
        get_score = ScoreTable.objects.get(student__id=student_obj.id, course__id=course_obj.id)
    except ObjectDoesNotExist:
        return ValidationError('No score for this student and id')
    
    if get_score.score == -1:
        return ValidationError('No score for this student and id')
    
    if get_score.reconsideration_status != 0:
        return ValidationError(f'ApReq has already been sent for this student and course.')
    return get_score