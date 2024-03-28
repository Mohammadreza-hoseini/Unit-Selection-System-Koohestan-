from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer


class StudentCreate(APIView):
    """
    API endpoint that allows student to be viewed or created.
    """

    def post(self, request, format=None):
        """
        Create a new Student.
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        """
        Return a list of all students.
        """
        students = Student.objects.all()
        # Serialize the queryset into JSON
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
