from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RequestOTPSerializer, ChangePasswordAction

class RequestOTPView(CreateAPIView):
    """
    API endpoint that send otp code for user email.
    """
    serializer_class = RequestOTPSerializer

    def perform_create(self, serializer):
        return Response("Code sent to your email address", status=status.HTTP_200_OK)


class ChangePassword(APIView):
    def post(self, request, format=None):
        """
        API endpoint that change password action.
        """
        serializer = ChangePasswordAction(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Your password has been successfully changed", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
