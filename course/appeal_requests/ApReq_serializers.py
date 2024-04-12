from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError



from accounts.models import Student
from course.models import ScoreTable
from term.models import Term
        
from .score_validations import validate_students_id, validate_prof_course_match, validate_term_match, validate_time, validate_scores

from .ApReq_validations import validate_term, validate_student_has_course, validate_score_and_ApReq_state

class ScoreTableSerializer(serializers.Serializer):
    students = serializers.ListField()
    scores = serializers.ListField()
    term = serializers.PrimaryKeyRelatedField(queryset=Term.objects.all())


    def validate(self, attrs):
        
        
        course_obj = self.context.get('course_obj')
        prof_obj = self.context.get('prof_obj')
        
        if len(attrs['students']) != len(attrs['scores']):
            raise ValidationError('number of students and scores do not match')
            
        validate_time(attrs['term'])
        validate_term_match(course_obj, prof_obj, attrs)
        validate_students_id(attrs, course_obj, attrs['term'])
        validate_prof_course_match(prof_obj, course_obj)
        validate_scores(attrs['scores'])

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        students = validated_data['students']
        scores = validated_data['scores']
        
        course_obj = self.context.get('course_obj')
        
        i = 0
        
        for student_id in students:
            get_student = Student.objects.get(id=student_id)
            score_data = {
                "student": get_student,
                "course": course_obj,
                "score": int(scores[i]),
            }
            ScoreTable.objects.create(**score_data)
            i += 1
        # return list of instances? #TODO
        
class ApReqHandler:
    def __init__(self, student_obj, course_obj, term_obj):
        
        self.term_obj = term_obj
        self.student_obj = student_obj
        self.course_obj = course_obj
        
        
    
    # TODO
    @transaction.atomic
    def update(self):
        
        valid_term = validate_term(self.student_obj, self.course_obj, self.term_obj)
        if isinstance(valid_term, Exception): # return raised exception
            return valid_term
        
        valid_student_course = validate_student_has_course(self.student_obj, self.course_obj, self.term_obj)
        if isinstance(valid_student_course, Exception):
            return valid_student_course
        
        valid_score_ApReqState = validate_score_and_ApReq_state(self.student_obj, self.course_obj)
        if isinstance(valid_score_ApReqState, Exception):
            return valid_score_ApReqState
        
        instance = valid_score_ApReqState
        instance.reconsideration_status = 2
        instance.save()
        return "ApReq added -> Reconsideration_state updated"
        