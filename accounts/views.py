from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Professor
from rest_framework import status
from .serializers import ProfessorSerializer


class ProfessorCreateView(APIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    def get(self, request, *args, **kwargs):
        professors = Professor.objects.all()
        serializer = self.serializer_class(professors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
