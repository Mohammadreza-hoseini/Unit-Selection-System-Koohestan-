from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView, CreateAPIView

from koohestan.utils.permission_handler import ITManagerPermission, StudentPermission
from .FilterSet import StudentModelFilter, EA_ModelFilter, ProfessorModelFilter
from .models import Student, EducationalAssistant, UserRole, Professor
from .serializers import (
    StudentSerializer,
    StudentGetDataSerializer,
    EducationalAssistantSerializer,
    ProfessorGetDataSerializer,
    EA_GetDataSerializer, RequestOTPSerializer, ChangePasswordAction, ProfessorSerializer
)


# Start code of Mohammadreza hoseini
class StudentCreate(APIView):
    """
    API endpoint that allows student to be created.
    """
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def post(self, request, format=None):
        """
        Create a new Student.
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllStudents(ListAPIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)
    """
    Return a list of all students.
    """
    serializer_class = StudentGetDataSerializer
    queryset = Student.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentModelFilter


class StudentGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)
    """
    API endpoint that allows student to be updated.
    """

    def put(self, request, pk):
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_student_serializer = StudentSerializer(data=request.data)
        if get_student_serializer.is_valid(raise_exception=True):
            get_student_serializer.update(
                instance=get_student, validated_data=get_student_serializer
            )
            return Response(get_student_serializer.data, status=status.HTTP_200_OK)
        return Response(
            get_student_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk):
        """
        Return a student.
        """
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_student_serializer = StudentGetDataSerializer(get_student)
        return Response(get_student_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Delete a student.
        """
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_student.student.delete()
        return Response("Successfully delete", status=status.HTTP_200_OK)


class RequestOTPView(CreateAPIView):
    """
    API endpoint that send otp code for user email.
    """
    serializer_class = RequestOTPSerializer

    def perform_create(self, serializer):
        return Response("Code sent to your email address", status=status.HTTP_200_OK)


class ChangePassword(APIView):
    def post(self, request, format=None):
        """
        API endpoint that change password action.
        """
        serializer = ChangePasswordAction(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Your password has been successfully changed", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# End code of Mohammadreza hoseini

class ProfessorCreate(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def post(self, request, format=None):
        serializer = ProfessorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessorGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def put(self, request, pk):
        try:
            get_professor = Professor.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This Professor does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_professor_serializer = ProfessorSerializer(data=request.data)
        if get_professor_serializer.is_valid(raise_exception=True):
            get_professor_serializer.update(
                instance=get_professor, validated_data=get_professor_serializer
            )
            return Response(get_professor_serializer.data, status=status.HTTP_200_OK)
        return Response(
            get_professor_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk):

        try:
            get_professor = Professor.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(
                "This Professor does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_professor_serializer = ProfessorGetDataSerializer(get_professor)
        return Response(get_professor_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            get_professor = Professor.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_professor.professor.delete()
        return Response('Successfully delete', status=status.HTTP_200_OK)


class GetAllProfessors(ListAPIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)
    serializer_class = ProfessorGetDataSerializer
    queryset = Professor.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfessorModelFilter


class EducationalAssistantView(APIView):

    def post(self, request):
        """
        Create a new EA -> Select from Professors
        """

        # Check if the user is IT-admin #TODO

        serializer = EducationalAssistantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAll_EAs(ListAPIView):
    """
        Return list of all EAs
    """

    serializer_class = EA_GetDataSerializer
    queryset = EducationalAssistant.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EA_ModelFilter


class EducationalAssistantWithPK(APIView):

    def get(self, request, pk):
        """
        Return an EA
        """
        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        serializer = EA_GetDataSerializer(EA_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an EA
        """

        # NOTE
        # possible #BUG

        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        serializer = EducationalAssistantSerializer(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=EA_obj, validated_data=serializer)
            return Response("Successfully updated", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an EA
        """
        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
            user_obj = UserRole.objects.get(id=EA_obj.assistant.professor.id)

        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        EA_obj.delete()

        user_obj.role = 2
        user_obj.save()

        return Response("Successfully deleted", status=status.HTTP_200_OK)



class Student_pass_courses_report(APIView):
    
    permission_classes = (IsAuthenticated, StudentPermission, )
    
    def get(self, request, pk):
        """
        Return passed courses of student
        """
        
        print("Salam")
        print(request.user.id)
        
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_200_OK)
    ...