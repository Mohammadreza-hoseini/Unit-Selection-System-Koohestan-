from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from accounts.models import Student
from koohestan.utils.permission_handler import StudentPermission, EducationalAssistantPermission
from term.Emergency_Removal.er_serializers import StudentEmergencyRemovalSerializer, \
    StudentGetDataEmergencyRemovalSerializer, AssistantEmergencyRemovalSerializer
from term.models import UnitRegisterRequest, EmergencyRemoval


class StudentEmergencyRemoval(APIView):
    """
    Send emergency removal request
    """

    permission_classes = (IsAuthenticated, StudentPermission,)

    def post(self, request, student_id, course_id):
        try:
            get_student = Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            return Response("This student does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            get_student_unit_request = UnitRegisterRequest.objects.get(student_id=student_id, course__id=course_id,
                                                                       term_id=get_student.term.id)
        except ObjectDoesNotExist:
            return Response("Student with this course does not exist", status=status.HTTP_404_NOT_FOUND)
        additional_data = {'get_student_unit_request': get_student_unit_request, 'course_id': course_id}
        serializer = StudentEmergencyRemovalSerializer(data=request.data, context=additional_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Emergency removal course Send Successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, student_id, course_id):
        try:
            get_student = Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            return Response("This student does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            get_emergency_removal_requests = EmergencyRemoval.objects.filter(student_id=student_id,
                                                                             course__id=course_id,
                                                                             term_id=get_student.term.id)
        except ObjectDoesNotExist:
            return Response('does not exist', status=status.HTTP_404_NOT_FOUND)
        get_student_serializer = StudentGetDataEmergencyRemovalSerializer(get_emergency_removal_requests, many=True)
        return Response(get_student_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, student_id, course_id):
        try:
            get_student = Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            return Response("This student does not exist", status=status.HTTP_404_NOT_FOUND)
        try:
            get_emergency_removal_requests = EmergencyRemoval.objects.filter(student_id=student_id,
                                                                             course__id=course_id,
                                                                             term_id=get_student.term.id)
        except ObjectDoesNotExist:
            return Response('does not exist', status=status.HTTP_404_NOT_FOUND)
        get_emergency_removal_requests.delete()
        return Response('deleted', status=status.HTTP_200_OK)


class AssistantAcceptOrRejectEmergencyRemoval(APIView):
    """
    Assistant accept or reject emergency removal request
    """

    permission_classes = (IsAuthenticated, EducationalAssistantPermission,)

    def post(self, request, assistant_id, emergency_removal_id):
        try:
            get_emergency_removal_request = EmergencyRemoval.objects.get(id=emergency_removal_id,
                                                                         assistant_id=assistant_id)
        except ObjectDoesNotExist:
            return Response("This request does not exist", status=status.HTTP_404_NOT_FOUND)
        additional_data = {'get_emergency_removal_request': get_emergency_removal_request}
        serializer = AssistantEmergencyRemovalSerializer(data=request.data, context=additional_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Emergency removal course Send Successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, assistant_id, emergency_removal_id):
        try:
            get_emergency_removal_request = EmergencyRemoval.objects.get(id=emergency_removal_id,
                                                                         assistant_id=assistant_id)
        except ObjectDoesNotExist:
            return Response("This request does not exist", status=status.HTTP_404_NOT_FOUND)

        get_student_serializer = StudentGetDataEmergencyRemovalSerializer(get_emergency_removal_request)
        return Response(get_student_serializer.data, status=status.HTTP_200_OK)


class AssistantGetAllAcceptOrRejectEmergencyRemoval(APIView):
    """
    Assistant GetAll accept or reject emergency removal request
    """

    permission_classes = (IsAuthenticated, EducationalAssistantPermission,)

    def get(self, request, assistant_id):
        get_emergency_removal_request = EmergencyRemoval.objects.filter(assistant_id=assistant_id)
        get_student_serializer = StudentGetDataEmergencyRemovalSerializer(get_emergency_removal_request, many=True)
        return Response(get_student_serializer.data, status=status.HTTP_200_OK)
