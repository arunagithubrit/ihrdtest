from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.response import Response

from users.serializers import LoginSerializer
from users.serializers import RegisterSerializer,UserSerializer

from core_viewsets.custom_viewsets import CreateViewSet
from core_viewsets.custom_viewsets import ListViewSet
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import authentication
from rest_framework import permissions


# Create your views here.


class RegisterViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):

        email = request.data.get('email')
        password = request.data.get('password', None)
        phone_number = request.data.get('phone_number')

        # TODO: Validations

        user = get_user_model().objects.create_user(request.data)

        return Response(
            {'code': 200, 'message': 'success', 'user_id': user._get_pk_val()},
        )


class LoginViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        # TODO: validation
        user=authenticate(email=email,password=password)
        # # if user:
        #     refresh=RefreshToken.for_user(user)
        #     data={
        #         'token':str(refresh.access_token),
        #     }
        #     return Response(data,status=status.HTTP_200_OK)
        # return Response({'error':}
        user_obj = get_user_model().objects.get(email=email, password=password)
        user_obj.last_login = timezone.now()
        if user:
            refresh=RefreshToken.for_user(user)
            data={
                'token':str(refresh.access_token),
            }
            return Response(
            {
                
                'code': 200,
                'message': 'success',
                'access_token': '',
                'refresh_token': 'refresh_token',
                'user_id': user_obj.pk,
                'name': user_obj.first_name,
                'email': user_obj.email,
                'last_login': user_obj.last_login,
            },
        )

            # return Response(data,status=status.HTTP_200_OK)
        # TODO:  generate token with jwt library
        # TODO: Update the Login activity

        # user_obj.last_login = timezone.now()
        # return Response(
        #     {
        #         'code': 200,
        #         'message': 'success',
        #         'access_token': '',
        #         'refresh_token': 'refresh_token',
        #         'user_id': user_obj.pk,
        #         'name': user_obj.first_name,
        #         'email': user_obj.email,
        #         'last_login': user_obj.last_login,
        #     },
        # )


class MeViewSet(ListViewSet):
    authentication_classes = ()  # ToDO Specify Auth class
    permission_classes = ()
    serializer_class =UserSerializer   # ToDO Specify serializer_class class
    queryset = get_user_model().objects.all()

    def list(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        obj=get_user_model().objects.get(id=id)
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data,instance=obj)
        # ToDO:  Add your code
        return Response(data=serializer.data)
