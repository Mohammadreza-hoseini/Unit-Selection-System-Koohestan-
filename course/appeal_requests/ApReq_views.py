from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from accounts.models import Student
from course.appeal_requests.ApReq_serializers import ScoreTableSerializer
from faculty.serializers import UniversityGetDataSerializer

from term.Unit_selection.unit_serializers import (
    URFormGetDataSerializer,
    URFormSerializer,
    SendFormSerializer,
    AcceptOrRejectFormSerializer
)
from term.models import UnitRegisterRequest


# UR -> UnitRegister
from .ApReq_validations import validate_students_id


class ScoreTableView(APIView):
    permission_classes = (IsAuthenticated,)


    # only the actual student #TODO
    def post(self, request):
        

        # additional_data = {'student_obj': get_student, 'URL_type': URL_type}
        
        print(request.data)
        serializer = ScoreTableSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print("yesss")
            serializer.save()
            return Response("Score added", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

