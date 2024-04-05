from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from koohestan.utils.permission_handler import ITManagerPermission
from .models import Faculty
from .serializers import (
    FacultySerializer, FacultyGetDataSerializer
)


class FacultyCreate(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllFaculty(ListAPIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)
    serializer_class = FacultyGetDataSerializer
    queryset = Faculty.objects.all()


class FacultyGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def put(self, request, pk):
        try:
            get_faculty = Faculty.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This Faculty does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_faculty_serializer = FacultySerializer(data=request.data)
        if get_faculty_serializer.is_valid(raise_exception=True):
            get_faculty_serializer.update(
                instance=get_faculty, validated_data=get_faculty_serializer
            )
            return Response(get_faculty_serializer.data, status=status.HTTP_200_OK)
        return Response(
            get_faculty_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk):
        try:
            get_faculty = Faculty.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This faculty does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_faculty_serializer = FacultyGetDataSerializer(get_faculty)
        return Response(get_faculty_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            get_faculty = Faculty.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This faculty does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_faculty.delete()
        return Response("Successfully delete", status=status.HTTP_200_OK)

