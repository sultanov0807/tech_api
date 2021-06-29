from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer, ActivationSerializer, LoginSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Вам на почту отпрален код подтверждения', status=status.HTTP_201_CREATED)

class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
        return Response('Ваш аккаунт успешно актевирован', status=status.HTTP_200_OK)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated ]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response('Вы успешно вышли')