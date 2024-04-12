from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from django_filters import rest_framework as filters

from course.models import Course, Subject
from koohestan.utils.permission_handler import ITManagerPermission, EducationalAssistantPermission
from .FilterSet import CourseModelFilter, SubjectModelFilter
from .serializers import CourseSerializer, CourseGetDataSerializer, SubjectSerializer, SubjectGetDataSerializer


# Start code of Mohammadreza hoseini
class SubjectCreate(APIView):
    """
    API endpoint that allows subject to be created.
    """
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def post(self, request):
        """
        Create a new Student.
        """
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllSubjects(ListAPIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)
    serializer_class = SubjectGetDataSerializer
    queryset = Subject.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubjectModelFilter


class SubjectGetUpdateDelete(APIView):

    def put(self, request, pk):
        try:
            get_subject = Subject.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "The subject does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_subject_serializer = SubjectSerializer(data=request.data)
        if get_subject_serializer.is_valid(raise_exception=True):
            get_subject_serializer.update(
                instance=get_subject, validated_data=get_subject_serializer
            )

            return Response(get_subject_serializer.data, status=status.HTTP_200_OK)
        return Response(
            get_subject_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk):
        try:
            get_subject = Subject.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "The subject does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_subject_serializer = SubjectGetDataSerializer(get_subject)
        return Response(get_subject_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            get_subject = Subject.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "The subject does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_subject.delete()
        return Response("Successfully delete", status=status.HTTP_200_OK)


# End code of Mohammadreza hoseini

class CourseView(APIView):
    """
    Create new course
    """
    
    #it should be its related educational assistant #BUG -> 
    permission_classes = (IsAuthenticated, ITManagerPermission, EducationalAssistantPermission)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAll_courses(ListAPIView):
    """
        Return list of all courses
    """
    
    permission_classes = (IsAuthenticated,)
    
    # everyone has access to it
    

    serializer_class = CourseGetDataSerializer
    queryset = Course.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseModelFilter


class CourseWithPK(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    
    def get_permissions(self):
        if self.request.method in ['PUT', "DELETE"]:
            return [ITManagerPermission, EducationalAssistantPermission]
        return super().get_permissions()
    
    # everyone has access to it
    def get(self, request, pk):
        """
        Return a course
        """
                
        try:
            course_obj = Course.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This course doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        serializer = CourseGetDataSerializer(course_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)



    # "only IT_Manager & related_EA can update a course"
    
    def put(self, request, pk):
        """
        Update a course
        """

        try:
            course_obj = Course.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This course doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=course_obj, validated_data=serializer)
            return Response("Successfully updated", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # "only IT_Manager & related_EA can delete a course"
    def delete(self, request, pk):
        """
        Delete a course
        """

        try:
            course_obj = Course.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This course doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        course_obj.delete()
        return Response("Successfully deleted", status=status.HTTP_200_OK)
