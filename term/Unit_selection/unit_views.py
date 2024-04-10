from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from accounts.models import Student
from faculty.serializers import UniversityGetDataSerializer
from koohestan.utils.permission_handler import (
    ITManagerPermission,
    EducationalAssistantPermission,
    StudentSelfPermission, StudentPermission, ProfessorPermission
)
from term.Unit_selection.unit_serializers import (
    URFormGetDataSerializer,
    URFormSerializer,
    SendFormSerializer,
    AcceptOrRejectFormSerializer
)
from term.models import UnitRegisterRequest


# UR -> UnitRegister


class URCreateView(APIView):
    permission_classes = (IsAuthenticated,)


    # only the actual student #TODO
    def post(self, request, st_pk):
        """
        Create UR_selection_form(or UR_substitution_form) for st_pk
        """
        
        URL_path = request.get_full_path()
        if 'selection' in URL_path:
            URL_type = 'selection'
        if 'substitution' in URL_path:
            URL_type = 'substitution'

        try:
            get_student = Student.objects.get(id=st_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Student does not exist", status=status.HTTP_404_NOT_FOUND
            )

        additional_data = {'student_obj': get_student, 'URL_type': URL_type}
        
        serializer = URFormSerializer(data=request.data, context=additional_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("UR_form created", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class URGetView(ListAPIView):
    """
    Get UR form of st_pk
    """

    # TODO
    # only professor & IT-admin ? #BUG possible
    permission_classes = (IsAuthenticated,)

    serializer_class = URFormGetDataSerializer
    queryset = UnitRegisterRequest.objects.all()


class URGetStPk(APIView):

    def get_permissions(self):
        # override it #TODO
        ...
        return super().get_permissions()

    # TODO
    # only professor and student  #BUG possible
    def get(self, request, st_pk):
        if not Student.objects.filter(id=st_pk).exists():
            return Response(
                "This Student does not exist", status=status.HTTP_404_NOT_FOUND
            )

        UR_forms_for_st_pk = UnitRegisterRequest.objects.filter(student__id=st_pk)

        if not UR_forms_for_st_pk.exists():
            return Response(
                "This Student does not have any UR_Form",
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = URFormGetDataSerializer(UR_forms_for_st_pk, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SendFormSelection(APIView):
    permission_classes = (IsAuthenticated, StudentPermission,)

    def post(self, request, st_pk):
        """
        Create UR form for st_pk
        """

        try:
            get_student = Student.objects.get(id=st_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Student does not exist", status=status.HTTP_404_NOT_FOUND
            )

        serializer = SendFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Form Send Successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptOrRejectForm(APIView):
    permission_classes = (IsAuthenticated, ProfessorPermission,)

    def post(self, request, st_pk, form_pk):
        """
        Create UR form for st_pk
        """
        try:
            get_form = UnitRegisterRequest.objects.get(id=form_pk)
        except ObjectDoesNotExist:
            return Response("This form does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            get_student = Student.objects.get(id=st_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Student does not exist", status=status.HTTP_404_NOT_FOUND
            )
        additional_data = {'student_obj': get_student, 'get_form': get_form}
        serializer = AcceptOrRejectFormSerializer(data=request.data, context=additional_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Form Send Successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #TODO
    # only professor & IT-admin ? #BUG possible
    permission_classes = (IsAuthenticated, )
    
    serializer_class = URFormGetDataSerializer
    queryset = UnitRegisterRequest.objects.all()