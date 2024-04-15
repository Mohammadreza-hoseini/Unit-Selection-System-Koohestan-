from rest_framework.exceptions import ValidationError
from accounts.models import StudentTermAverage
from course.models import Course
from django.db.models import F
from django.db.models import Max
from django.utils import timezone

from term.models import UnitRegisterRequest


def validate_passed_course(attrs, student_obj):
    """
    Check if course's subject has already been passed
    """
    passed_lessons = student_obj.passed_lessons
    course = attrs["course"]

    for course_id in course:

        get_course = Course.objects.filter(id=course_id).first()
        if not get_course:
            raise ValidationError(f"{course_id} course doesn't exist")

        subject_id = get_course.subject.id
        subject_name = get_course.subject.name

        if passed_lessons.filter(id=subject_id).exists():
            raise ValidationError(
                f"{subject_name} has been passed -> course_id: {course_id}"
            )


def validate_course_capacity(attrs):
    course = attrs["course"]

    for course_id in course:
        course_obj = Course.objects.get(id=course_id)
        if course_obj.capacity <= 0:
            raise ValidationError(f"No more capacity for {course_id} course")


def validate_student_add_unit_average(attrs, student_obj):
    course = attrs["course"]
    get_student = StudentTermAverage.objects.filter(student=student_obj)
    max_units_selection = 0
    if get_student.exists():
        get_student_average = get_student.order_by(F('id').desc()).last()

        # If we don't have student's average (due to DB ...)
        if get_student_average.average is None:
            max_units_selection = 24
        elif get_student_average.average >= 17:
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
        raise ValidationError(
            "The number of your course units is more than the allowed limit"
        )
        
    if sum_units_selection < 12:
        raise ValidationError(
            "The number of your course units should be at least 12"
        )
    


def validate_exam_and_class_time_interference(attrs):
    course = attrs["course"]
    for item in course:
        get_course = Course.objects.filter(id=item).first()
        if get_course.time == get_course.exam_time.time():
            raise ValidationError('Class time interferes with exam time')


def validate_courses_related_to_the_field(attrs, student_obj):
    course = attrs["course"]
    for item in course:
        get_course = Course.objects.filter(id=item).first().subject.provider_faculty.id
        if get_course != student_obj.faculty.id:
            raise ValidationError('The selected course is not related to the faculty')


def subject_prerequisites(subject, passed_lessons):
    """
    check prerequisites for specific course's subject
    """

    prerequisite = subject.prerequisite.all()
    not_passed_subjects = []
    for pre_subject in prerequisite:
        # check passed or not
        passed = passed_lessons.filter(id=pre_subject.id).exists()
        if not passed:
            not_passed_subjects.append(pre_subject.name)
    return not_passed_subjects


def validate_prerequisite_subject_passed(attrs, student_obj):
    # consider taking both corequisite-subject and main-subject #TODO
    
    passed_lessons = student_obj.passed_lessons
    course = attrs["course"]

    for course_id in course:
        get_course = Course.objects.get(id=course_id)
        get_subject = get_course.subject
        not_passed_subjects = subject_prerequisites(get_subject, passed_lessons)
        if len(not_passed_subjects) != 0:
            raise ValidationError(f'Prerequisites of {course_id} course is not satisfied \
                                    not_passed_subjects: subjects: {not_passed_subjects}'
                                    )
            
def validate_Student_URForm_Term(term_id, student_id):
    already_exist_form = UnitRegisterRequest.objects.filter(term__id=term_id, student__id=student_id).first()
    return already_exist_form


def UR_update_delete(pre_URForm):
    #  add 1 capacity to already_exist_form.courses
    pre_courses = pre_URForm.course.all()
    for released_course in pre_courses:
        released_course.capacity += 1
        released_course.save()


def validate_St_current_term_UR(attrs, student_obj):
    """
    Student can only make URForm for its current term
    """
    UR_term = attrs['term'].id
    St_current_term = student_obj.term.id
    if UR_term != St_current_term:
        raise ValidationError('UR_term does not match St_current_term')
    
def validate_UR_selection_time(attrs):
    term = attrs['term']
    selection_end_time = term.end_selection_time 
    selection_start_time = term.start_selection_time
    if not selection_start_time < timezone.now() < selection_end_time:
        raise ValidationError('Time rule: start_selection_time < now < end_selection_time')


def validate_checking_student_years(attrs, student_obj):
    get_max_term_number = student_obj.student_term_average_student.values('term_number').aggregate(Max('term_number'))
    if get_max_term_number['term_number__max'] > 8:
        raise ValidationError('Your academic years are over')


def validate_doped_AddOrDelete_UnitLimit(previous_URform, substitution_URform):
    """
    Substitution_URform:
        -) At most 2 courses can be deleted and added
        -) At most 6 number of units can be deleted and added
    """
    added_total_unit_number = 0
    deleted_total_unit_number = 0


    substitute_courses = substitution_URform.course.all()
    previous_courses = previous_URform.course.all()
    
    number_of_added_courses = 0
    number_of_deleted_courses = 0
    
    # Check courses that haven't been in the previous UR_form
    for new_course_id in substitute_courses:
        get_course = Course.objects.get(id=new_course_id)
        course_unit_number = get_course.subject.number_of_course
        check_new_added = previous_courses.filter(id=new_course_id).exists()
        
        # if the course has been added
        if check_new_added:
            number_of_added_courses += 1
            added_total_unit_number +=  course_unit_number
            
    # Check courses that haven been in the previous UR_form but not in substitution_URform
    for pre_course_id in previous_courses:
        get_course = Course.objects.get(id=pre_course_id)
        course_unit_number = get_course.subject.number_of_course
        check_remained = substitute_courses.filter(id=pre_course_id).exists()
        
        # if the course has been deleted
        if not check_remained:
            number_of_deleted_courses += 1
            deleted_total_unit_number +=  course_unit_number
    
    if number_of_added_courses > 2:
        raise ValidationError('2 courses can Be added at most')
    if number_of_deleted_courses > 2:
        raise ValidationError("2 courses can Be deleted at most")
    
    
    if added_total_unit_number > 6:
        raise ValidationError('unit_number of new added subjects in substitution_form should be at most 6')
    if deleted_total_unit_number > 6:
        raise ValidationError('unit_number of deleted subjects in substitution_form should be at most 6')
    
    
def validate_doped_selection_time(attrs):
    term = attrs['term']
    substitution_start_time = term.doped_added_start_time 
    substitution_end_time = term.doped_added_end_time
    if not substitution_start_time < timezone.now() < substitution_end_time:
        raise ValidationError('Time rule: doped_added_start_time < now < doped_added_end_time')
    
def validate_course_term(attrs):
    course = attrs["course"]
    term_id = attrs['term'].id

    for course_id in course:
        course_obj = Course.objects.get(id=course_id)
        if course_obj.term.id != term_id:
            raise ValidationError(f"{course_id} course is not for this term")