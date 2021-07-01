from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import *

# 1. Регистрация
class RegView(APIView):
    def post(self, request):
        serializer = RegSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Вам на почту отпрален код подтверждения', status=status.HTTP_201_CREATED)

# 2. Активация
class ActView(APIView):
    def post(self, request):
        serializer = ActSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
        return Response('Ваш аккаунт успешно актевирован', status=status.HTTP_200_OK)

# 3. Логин
class LogView(ObtainAuthToken):
    serializer_class = LogSerializer


class OutView(APIView):
    permission_classes = [IsAuthenticated ]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response('Вы успешно вышли')


# 4. Восстановление пароля
class RestPassView(APIView):
    def post(self, request):
        serializer = RestPassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_message()
            return Response('Вам отправлен код для смены пароля', status=status.HTTP_200_OK)