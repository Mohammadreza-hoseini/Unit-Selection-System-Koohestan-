from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from django_filters import rest_framework as filters

from course import views
from course.models import Course, Subject
from koohestan.utils.permission_handler import ITManagerPermission, EducationalAssistantPermission

# UR -> UnitRegister


class UR_CreateView(APIView):
    
    def post(self, request, st_pk):
        """
        Create UR form for st_pk
        """
        ...
    
    
class UR_GetView(ListAPIView):
    """
    Get UR form of st_pk
    """
    ...
    
    
    