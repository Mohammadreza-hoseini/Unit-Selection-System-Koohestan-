from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from accounts.models import Professor, Student
from course.appeal_requests.ApReq_serializers import ApReqHandler, ScoreTableHandler
from course.models import Course

from term.models import Term


# UR -> UnitRegister


class ScoreTableView(APIView):
    permission_classes = (IsAuthenticated,)


    # only the actual student #TODO
    def post(self, request, pr_pk, course_pk):
        
        try:
            get_prof = Professor.objects.get(id=pr_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Professor does not exist", status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            get_course = Course.objects.get(id=course_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Course does not exist", status=status.HTTP_404_NOT_FOUND
            )
        
        students = request.data['students']
        scores = request.data['scores']
        term = request.data['term']
        
        
        scores = ScoreTableHandler(students, scores, term, get_prof, get_course)
        res = scores.validate()
        
        if isinstance(res, Exception):
            return Response(str(res), status=status.HTTP_400_BAD_REQUEST)

        return Response(f"{res} added", status=status.HTTP_200_OK)


class ApReqView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def put(self, request, st_pk, course_pk):
        try:
            get_student = Student.objects.get(id=st_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Student does not exist", status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            get_course = Course.objects.get(id=course_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Course does not exist", status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            get_term = Term.objects.get(id=request.data['term'])
        except ObjectDoesNotExist:
            return Response(
                "This Term does not exist", status=status.HTTP_404_NOT_FOUND
            )
        
        ApReq = ApReqHandler(student_obj=get_student, course_obj=get_course, term_obj=get_term)
        res = ApReq.update()
        
        if isinstance(res, Exception):
            return Response(str(res), status=status.HTTP_400_BAD_REQUEST)
        
        return Response("ApReq sent successfully", status=status.HTTP_200_OK)
        