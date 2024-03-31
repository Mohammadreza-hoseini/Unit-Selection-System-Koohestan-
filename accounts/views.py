from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, EducationalAssistant
from .serializers import (
    StudentSerializer,
    StudentGetDataSerializer,
    EducationalAssistantSerializer,
)


class StudentGetCreate(APIView):
    """
    API endpoint that allows student to be created.
    """

    def post(self, request, format=None):
        """
        Create a new Student.
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        """
        Return a list of all students.
        """
        students = Student.objects.all()
        serializer = StudentGetDataSerializer(students, many=True)
        return Response(serializer.data)


class StudentGetUpdateDelete(APIView):
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
            return Response(status=status.HTTP_200_OK)
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


class EducationalAssistantView(APIView):
    def post(self, request):
        """
        Create a new EA -> Select from Professors
        """

        # Check if the user is IT-admin #TODO

        # filtering based on project documentation #TODO

        # request.data is only the national_code #BUG
        serializer = EducationalAssistantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Return list of all EAs
        """
        EAs = EducationalAssistant.objects.all()
        serializer = EducationalAssistantSerializer(EAs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EducationalAssistantWithPK(APIView):
    def get(self, request, pk):
        """
        Return an EA
        """
        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        serializer = EducationalAssistantSerializer(EA_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an EA
        """

        # EA update fields #QUESTION

        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        serializer = EducationalAssistantSerializer(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=EA_obj, validated_data=serializer)
            return Response("Invalid data", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an EA
        """
        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        # change user's role back to 'professor' #TODO
        EA_obj.delete()

        return Response('Successfully deleted', status=status.HTTP_200_OK)