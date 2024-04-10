from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from koohestan.utils.permission_handler import StudentSelfPermission, ITManagerPermission

from accounts.models import Student
from accounts.St.st_serializers import StudentSerializer, StudentGetDataSerializer, ST_Passed_Courses_Serializer, \
    ST_Progress_Courses_Serializer

from accounts.FilterSet import StudentModelFilter


class StudentTermCourses(APIView):
    permission_classes = (IsAuthenticated, StudentSelfPermission,)

    def get(self, request, pk):
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "There is no student", status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ST_Progress_Courses_Serializer(get_student)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentPassedCourses_PK(APIView):
    """
    Return student's passed_courses
    """

    permission_classes = (IsAuthenticated, StudentSelfPermission,)

    def get(self, request, pk):
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ST_Passed_Courses_Serializer(get_student)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        get_student_serializer = StudentGetDataSerializer(get_student, many=True)
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
