from rest_framework.exceptions import ValidationError
from accounts.models import StudentTermAverage
from course.models import Course
from django.db.models import F


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
            
# corequisite delete validation -> symmetrical = False in 'Subject' model? #TODO
# course delete method in UR #TODO 
# can't add a course in UR_form more than once #TODO