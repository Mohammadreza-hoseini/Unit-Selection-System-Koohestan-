# from weasyprint import HTML
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import Student
from course.serializers import CourseGetDataSerializer
from koohestan.tasks import sending_busy_studying_pdf
from koohestan.utils.permission_handler import StudentPermission, EducationalAssistantPermission
from term.models import BusyStudyingRequest, UnitRegisterRequest
from term.serializers import BusyStudyingRequestSerializer, BusyStudyingRequestGetDataSerializer, \
    BusyStudyingRequestAcceptOrRejectSerializer, UnitRegisterRequestSerializer


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
            get_busy_studying_request = BusyStudyingRequest.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(
                "This Busy Studying Request does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_busy_studying_request_serializer = BusyStudyingRequestGetDataSerializer(get_busy_studying_request)
        return Response(get_busy_studying_request_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            get_busy_studying_request = BusyStudyingRequest.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This Busy Studying Request does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_busy_studying_request.delete()
        return Response('Successfully delete', status=status.HTTP_200_OK)


class BusyStudyingRequestAcceptOrReject(APIView):
    permission_classes = (IsAuthenticated, EducationalAssistantPermission,)

    def get(self, request, assistant_id, studying_id):
        try:
            get_assistant = BusyStudyingRequest.objects.get(id=studying_id, assistant_id=assistant_id)
        except ObjectDoesNotExist:
            return Response('This Studying id with this assistant id does not exist', status=status.HTTP_404_NOT_FOUND)
        serializer = BusyStudyingRequestGetDataSerializer(get_assistant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, assistant_id, studying_id):
        try:
            busy_studying_request = BusyStudyingRequest.objects.get(id=studying_id, assistant_id=assistant_id)
        except ObjectDoesNotExist:
            return Response('This Studying id with this assistant id does not exist', status=status.HTTP_404_NOT_FOUND)
        additional_data = {'busy_studying_request': busy_studying_request}
        serializer = BusyStudyingRequestAcceptOrRejectSerializer(data=request.data, context=additional_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if serializer.validated_data['request_state'] == 2:
                # Generate PDF
                html_string = render_to_string('term/busy_studying_request.html',
                                               {'busy_studying_request_data': serializer.context[
                                                   'busy_studying_request']})
                pdf_file = HTML(string=html_string).write_pdf()
                sending_busy_studying_pdf(serializer.context['busy_studying_request'], pdf_file)
            return Response("done successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EducationalAssistantGetAllBusyStudyingRequest(APIView):
    permission_classes = (IsAuthenticated, EducationalAssistantPermission,)

    def get(self, request, assistant_id):
        assistant_get_all_busy_studying_request = BusyStudyingRequest.objects.filter(assistant_id=assistant_id)
        if not assistant_get_all_busy_studying_request.exists():
            return Response('This Studying id with this assistant id does not exist', status=status.HTTP_404_NOT_FOUND)
        serializer = BusyStudyingRequestGetDataSerializer(assistant_get_all_busy_studying_request, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnitRegisterRequestGetData(APIView):
    permission_classes = (IsAuthenticated, StudentPermission,)

    def get(self, request, pk):

        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("this student does not exist.", status=status.HTTP_404_NOT_FOUND)

        try:
            get_course = UnitRegisterRequest.objects.get(student=get_student, term=get_student.term,
                                                         request_state=2).course.all()
        except ObjectDoesNotExist:
            return Response('this course does not exist.', status=status.HTTP_404_NOT_FOUND)

        return Response(CourseGetDataSerializer(get_course, many=True).data, status=status.HTTP_200_OK)


class StudentDetails(APIView):
    def get(self, request, pk):
        get_student = UnitRegisterRequest.objects.filter(supervisor_id=pk)
        if not get_student.exists():
            return Response(
                'There is no student for this professor', status=status.HTTP_404_NOT_FOUND
            )
        get_student_detail = UnitRegisterRequestSerializer(get_student, many=True)
        return Response(get_student_detail.data, status=status.HTTP_200_OK)


class GetStudentData(APIView):
    def get(self, request, pr_pk, st_pk):
        try:
            get_student = UnitRegisterRequest.objects.filter(supervisor_id=pr_pk, student_id=st_pk)
        except ObjectDoesNotExist:
            return Response(
                'There is no student of professor whit information like this', status=status.HTTP_404_NOT_FOUND
            )
        get_student = UnitRegisterRequestSerializer(get_student, many=True)
        return Response(get_student.data, status=status.HTTP_200_OK)
