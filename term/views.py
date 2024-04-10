from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from accounts.models import Student
from term.models import BusyStudyingRequest
from term.serializers import BusyStudyingRequestSerializer, busystudyingrequestGetDataSerializer


class BusyStudyingRequestCreatGetUpdateDelete(APIView):

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

    def put(self, request, pk):
        try:
            get_BusyStudyingRequest = BusyStudyingRequest.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This Busy Studying Request does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_BusyStudyingRequest_serializer = BusyStudyingRequest(data=request.data)
        if get_BusyStudyingRequest_serializer.is_valid(raise_exception=True):
            get_BusyStudyingRequest_serializer.update(
                instance=get_BusyStudyingRequest, validated_data=get_BusyStudyingRequest_serializer
            )
            return Response(get_BusyStudyingRequest_serializer.data, status=status.HTTP_200_OK)
        return Response(
            get_BusyStudyingRequest_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk):

        try:
            get_BusyStudyingRequest = BusyStudyingRequest.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(
                "This Busy Studying Request does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_BusyStudyingRequestSerializer = busystudyingrequestGetDataSerializer(get_BusyStudyingRequest)
        return Response(get_BusyStudyingRequestSerializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            get_BusyStudyingRequest = BusyStudyingRequest.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This Busy Studying Request does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_BusyStudyingRequest.BusyStudyingRequest.delete()
        return Response('Successfully delete', status=status.HTTP_200_OK)
