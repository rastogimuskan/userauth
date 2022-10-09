from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, logout
from .serializers import UserRegistrationSerializers, UserLoginSerializers, UserProfileSerializer, UsercChangePasswordSerializer, ShowDynamicSerializer
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import links
import json

from django.core import serializers

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):

    renderer_classes = [UserRenderer]

    def post(self, request, format=None):

        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    renderer_classes = [UserRenderer]
    def post(self, request, format=None):

        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            token = get_tokens_for_user(user)
            if user:
                return Response({'token':token,'msg': 'Log in successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors':['Email or Password not found']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsercChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer =  UsercChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password changed successful'}, status=status.HTTP_200_OK)

class UserLogout(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response('User Logged out successfully')

class ShowDynamicLinks(APIView):
    def post(self, request, format=None):
        queryset = links.objects.all()
        # queryset = json.dumps(queryset)
        serializer_class = ShowDynamicSerializer(queryset)
        tmpJson = serializers.serialize("json", queryset)
        tmpObj = json.loads(tmpJson)
        queryset = json.dumps(tmpObj)
        if request.user.is_admin:
            return Response({'msg': 'User is allowed','links':queryset})
        else:
            return Response('User is not allowed to see the links')



        

