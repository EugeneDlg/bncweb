import re

from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Visitors, TestAPI
from .serializers import UserSerializer, TestAPISerializer


def login_view(request):
    if request.method == 'POST':
        # form = MyAuthForm(data=request.POST)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            # return render(request, 'home.html', {'capacity': request.game.capacity})
            else:
                return redirect('signup')
        else:
            response = render(request, 'login.html', {'form': form})
            response.status_code = 401
            return response
    else:
        ip_address = get_ip_address(request)
        client_info = request.META['HTTP_USER_AGENT']
        match = re.search(r'.* \((.*)\)\s+(.*)', client_info)
        if match is not None:
            client_os = match.group(1).strip()
            client_browser = match.group(2).strip()
            visitor = Visitors.objects.create(
                ip_address=ip_address,
                os=client_os,
                browser=client_browser,
                time=timezone.now(),
            )
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def get_ip_address(request):
    client_ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if client_ip:
        ip_address = client_ip.split(',')[-1]
    else:
        ip_address = request.META.get("REMOTE_ADDR")
    return ip_address


class GetUsersView(APIView):
    # @swagger_auto_schema(
    #     tags=['User info'],
    #     operation_id='Get user info',
    #     operation_description='Get info about all users',
    #     responses={
    #         '200': 'OK',
    #         '400': 'Bad request'
    #     },
    #     # request_body=openapi.Schema(
    #     #     type=openapi.TYPE_OBJECT,
    #     #     properties={
    #     #         'users ids': openapi.Schema(type=openapi.TYPE_INTEGER, description='users ids'),
    #     #     }
    #     # )
    # )
    def get(self, request):
        qs = User.objects.all()
        serializer_for_qs = UserSerializer(instance=qs, many=True)
        return Response(serializer_for_qs.data)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        print("POST")
        print(data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UsersViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     http_method_names = ('get', 'post', 'patch', 'delete')


class TestAPIView(APIView):
    def get(self, request):
        qs = TestAPI.objects.all()
        serializer_for_qs = TestAPISerializer(instance=qs, many=True)
        return Response(serializer_for_qs.data)

    def post(self, request):
        data = request.data
        serializer = TestAPISerializer(data=data, many=True)
        print(data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


