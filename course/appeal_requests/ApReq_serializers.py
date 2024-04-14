from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError



from accounts.models import Student
from course.models import ScoreTable
from term.models import Term
        
from .score_validations import validate_students_id, validate_prof_course_match, validate_term_match, validate_time, validate_scores, check_term

from .ApReq_validations import validate_term, validate_student_has_course, validate_score_and_ApReq_state

class ScoreTableHandler:
    
    
    def __init__(self, students, scores, term, prof_obj, course_obj):
        self.students = students
        self.scores = scores
        self.term = check_term(term)
         
        self.prof_obj = prof_obj
        self.course_obj = course_obj


    def validate(self):
        
        if len(self.students) != len(self.scores):
            raise ValidationError('number of students and scores do not match')
            
        valid_time = validate_time(self.term)
        if isinstance(valid_time, Exception): # return raised exception
            return valid_time
        
        
        valid_term_match = validate_term_match(self.course_obj, self.prof_obj, self.term)
        if isinstance(valid_term_match, Exception): # return raised exception
            return valid_term_match
        
        valid_student = validate_students_id(self.students, self.course_obj, self.term)
        if isinstance(valid_student, Exception): # return raised exception
            return valid_student
        
        
        valid_prof_course = validate_prof_course_match(self.prof_obj, self.course_obj)
        if isinstance(valid_prof_course, Exception): # return raised exception
            return valid_prof_course
        
        
        valid_scores = validate_scores(self.scores)
        if isinstance(valid_scores, Exception): # return raised exception
            return valid_scores

        return self.create()

    @transaction.atomic
    def create(self):        
        i = 0
        
        new_scores = []
        for student_id in self.students:
            get_student = Student.objects.get(id=student_id)
            score_data = {
                "student": get_student,
                "course": self.course_obj,
                "score": int(self.scores[i]),
            }
            new_scores.append(ScoreTable(**score_data))
            i += 1
        return ScoreTable.objects.bulk_create(new_scores)
        
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
        