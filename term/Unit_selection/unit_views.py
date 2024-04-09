from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from accounts.models import Student
from koohestan.utils.permission_handler import ITManagerPermission, EducationalAssistantPermission, StudentSelfPermission
from term.Unit_selection.unit_serializers import URFormGetDataSerializer, URFormSerializer
from term.models import UnitRegisterRequest


# UR -> UnitRegister


class URCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, st_pk):
        """
        Create UR form for st_pk
        """

        try:
            get_student = Student.objects.get(id=st_pk)
        except ObjectDoesNotExist:
            return Response(
                "This Student does not exist", status=status.HTTP_404_NOT_FOUND
            )

        additional_data = {'student_obj': get_student}

        serializer = URFormSerializer(data=request.data, context=additional_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("UR_form created", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class URGetView(ListAPIView):
    """
    Get UR form of st_pk
    """
    
    permission_classes = (IsAuthenticated, )
    
    serializer_class = URFormGetDataSerializer
    queryset = UnitRegisterRequest.objects.all()
    
    def get_queryset(self):
        print("here")
        st_pk = self.kwargs.get('st_pk')
        print(st_pk)
        UR_forms_for_st_pk = self.queryset.filter(student__id=st_pk)
        print(UR_forms_for_st_pk)
        return UR_forms_for_st_pk
        
        ...
        # return super().get_queryset()
    ...

class URGetUpdateDelete(APIView):
    
    def get_permissions(self):
        # override it #TODO
        ...
        # return super().get_permissions()
    def put(self, request, pk):
        #TODO
        ...

    def get(self, request, pk):
        #TODO
        ...

    def delete(self, request, pk):
       #TODO 
        ...