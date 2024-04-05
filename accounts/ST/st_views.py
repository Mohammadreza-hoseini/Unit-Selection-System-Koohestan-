from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.ST.st_serializers import ST_Passed_Courses_GET
from koohestan.utils.permission_handler import StudentSelfPermission
from ..models import Student

class StudentPassedCourses_PK(APIView):
    
    permission_classes = (IsAuthenticated, StudentSelfPermission, )
    
    def get(self, request, pk):
        try:
            get_student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ST_Passed_Courses_GET(get_student)
        return Response(serializer.data, status=status.HTTP_200_OK)