from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from accounts.models import Student
from koohestan.utils.permission_handler import ITManagerPermission, EducationalAssistantPermission, StudentSelfPermission
from term.Unit_selection.unit_serializers import UR_Form_Serializer

# UR -> UnitRegister


class UR_CreateView(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, st_pk):
        """
        Create UR form for st_pk
        """

        try:
            get_student =  Student.objects.get(id=st_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Student does not exist", status=status.HTTP_404_NOT_FOUND
            )
        
        additional_data = {'student_obj': get_student}

        serializer = UR_Form_Serializer(data=request.data, context=additional_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("UR_form created", status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UR_GetView(ListAPIView):
    """
    Get UR form of st_pk
    """
    ...
    
    
    