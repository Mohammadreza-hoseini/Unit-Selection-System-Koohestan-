from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters


from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.FilterSet import EA_ModelFilter

from koohestan.utils.permission_handler import StudentSelfPermission, ITManagerPermission

from accounts.models import  EducationalAssistant, UserRole
from accounts.EA.ea_serializers import EducationalAssistantSerializer, EA_GetDataSerializer


class EducationalAssistantView(APIView):
    
    permission_classes = (IsAuthenticated, ITManagerPermission, )
    
    def post(self, request):
        """
        Create a new EA -> Select from Professors
        """

        # Check if the user is IT-admin #TODO

        serializer = EducationalAssistantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAll_EAs(ListAPIView):
    """
        Return list of all EAs
    """
    permission_classes = (IsAuthenticated, ITManagerPermission, )
    serializer_class = EA_GetDataSerializer
    queryset = EducationalAssistant.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EA_ModelFilter


class EducationalAssistantWithPK(APIView):



    def get(self, request, pk):
        """
        Return an EA
        """
        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        serializer = EA_GetDataSerializer(EA_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an EA
        """

        # NOTE
        # possible #BUG

        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        serializer = EducationalAssistantSerializer(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=EA_obj, validated_data=serializer)
            return Response("Successfully updated", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an EA
        """
        try:
            EA_obj = EducationalAssistant.objects.get(id=pk)
            user_obj = UserRole.objects.get(id=EA_obj.assistant.professor.id)

        except ObjectDoesNotExist:
            return Response("This EA doesn't exist", status=status.HTTP_400_BAD_REQUEST)

        EA_obj.delete()

        user_obj.role = 2
        user_obj.save()

        return Response("Successfully deleted", status=status.HTTP_200_OK)