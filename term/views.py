from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from koohestan.utils.permission_handler import ITManagerPermission

from rest_framework.permissions import IsAuthenticated

from .FilterSet import TermModelFilter
from .models import Term
from .serializers import TermSerializer, TermGetDataSerializer


# IT-admin access
class TermView(APIView):
    """
    Create new Term
    """

    permission_classes = (IsAuthenticated, ITManagerPermission,)
    
    def post(self, request):
        serializer = TermSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# IT-admin access
class GetAll_terms(ListAPIView):
    """
        Return list of all terms
    """
    permission_classes = (IsAuthenticated, )
    
    serializer_class = TermGetDataSerializer
    queryset = Term.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TermModelFilter

# IT-admin access
class TermWithPK(APIView):
    
    
    def get_permissions(self):
        print(self.request.user.username)
        if self.request.method in ['PUT', 'DELETE']:
            return (IsAuthenticated(), ITManagerPermission(), )
        return (IsAuthenticated(), )
    
    def get(self, request, pk):
        print("rrrrrrrrrrrrrrrrrrr")
        """
        Return a term
        """
        try:
            term_obj = Term.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This Term doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        serializer = TermGetDataSerializer(term_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        """
        Update a term
        """
        
        try:
            term_obj = Term.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This Term doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TermSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=term_obj, validated_data=serializer)
            return Response("Successfully updated", status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        """
        Delete a term
        """
        
        try:
            term_obj = Term.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("This Term doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        term_obj.delete()
        return Response("Successfully deleted", status=status.HTTP_200_OK)