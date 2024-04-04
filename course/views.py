from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
    permission_classes = (IsAuthenticated, ITManagerPermission, EducationalAssistantPermission,)

    def post(self, request):
        """
        Create a new Student.
        """
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllSubjects(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)
    serializer_class = SubjectGetDataSerializer
    queryset = Subject.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubjectModelFilter



# End code of Mohammadreza hoseini

class CourseView(APIView):
    """
    Create new course
    """

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

    serializer_class = CourseGetDataSerializer
    queryset = Course.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseModelFilter


class CourseWithPK(APIView):
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
