from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters


from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from koohestan.utils.permission_handler import ITManagerPermission, ProfessorSelfPermission, ProfessorSelf_ITPermission
from accounts.FilterSet import ProfessorModelFilter


from accounts.models import Professor

from accounts.Pr.pr_serializers import (
    ProfessorGetDataSerializer,
    ProfessorSerializer
)

class ProfessorCreate(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def post(self, request, format=None):
        serializer = ProfessorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessorGetUpdateDelete(APIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)

    def get_permissions(self):
        print(self.request.method)
        if self.request.method == 'DELETE':
            return (IsAuthenticated(), ITManagerPermission(), )
        if self.request.method == 'PUT':
            return (IsAuthenticated(), ProfessorSelf_ITPermission(),)
        return (IsAuthenticated(), )

    def put(self, request, pk):
        try:
            get_professor = Professor.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This Professor does not exist", status=status.HTTP_404_NOT_FOUND
            )
        get_professor_serializer = ProfessorSerializer(data=request.data)
        if get_professor_serializer.is_valid(raise_exception=True):
            get_professor_serializer.update(
                instance=get_professor, validated_data=get_professor_serializer
            )
            return Response(get_professor_serializer.data, status=status.HTTP_200_OK)
        return Response(
            get_professor_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, pk):

        try:
            get_professor = Professor.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(
                "This Professor does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_professor_serializer = ProfessorGetDataSerializer(get_professor)
        return Response(get_professor_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            get_professor = Professor.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "This student does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        get_professor.professor.delete()
        return Response('Successfully delete', status=status.HTTP_200_OK)


class GetAllProfessors(ListAPIView):
    permission_classes = (IsAuthenticated, ITManagerPermission,)
    serializer_class = ProfessorGetDataSerializer
    queryset = Professor.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfessorModelFilter
