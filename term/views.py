from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import Student
from koohestan.utils.permission_handler import StudentPermission
from term.models import BusyStudyingRequest
from term.serializers import BusyStudyingRequestSerializer, BusyStudyingRequestGetDataSerializer


class BusyStudyingRequestCreatGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated, StudentPermission,)

    def post(self, request, pk):
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("this student does not exist.", status=status.HTTP_404_NOT_FOUND)
        serializer = BusyStudyingRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):

        try:
            get_BusyStudyingRequest = BusyStudyingRequest.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(
                "This Busy Studying Request does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_BusyStudyingRequestSerializer = BusyStudyingRequestGetDataSerializer(get_BusyStudyingRequest)
        return Response(get_BusyStudyingRequestSerializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            get_BusyStudyingRequest = BusyStudyingRequest.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This Busy Studying Request does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_BusyStudyingRequest.delete()
        return Response('Successfully delete', status=status.HTTP_200_OK)
