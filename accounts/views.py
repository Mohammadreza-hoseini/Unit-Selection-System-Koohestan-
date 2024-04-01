from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView

from .FilterSet import StudentModelFilter, EA_ModelFilter
from .models import Student, EducationalAssistant, UserRole
from .serializers import (
    StudentSerializer,
    StudentGetDataSerializer,
    EducationalAssistantSerializer,
    EA_GetDataSerializer
)


class StudentCreate(APIView):
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


class GetAllStudents(ListAPIView):
    """
    Return a list of all students.
    """
    serializer_class = StudentGetDataSerializer
    queryset = Student.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentModelFilter


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
            return Response("Invalid data", status=status.HTTP_200_OK)
        
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
