"""
API
This file contains the logic of CRUD for the API of users.
"""
import django.contrib.auth.admin

from django.shortcuts import get_object_or_404
import drf_spectacular.utils
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from apps.users.models import ExploitationUser, User
from apps.users.api.serializers import (
    ExploitationUserSerializer, ResponseUserSerializer, UserSerializer, UserListSerializer, UpdateUserSerializer,
    PasswordSerializer, RequestUserSerializer
)

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiRequest, OpenApiExample, OpenApiTypes
from drf_spectacular.types import OpenApiTypes

class UserPasswordViewSet(viewsets.GenericViewSet):
    """
    User Password Set for User
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    serializer_class = PasswordSerializer
    queryset = None
    
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        """
        Set Password
        This method is used to set a new password.
        """
        user = request.user
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Contraseña actualizada correctamente'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class UserViewAdminSet(viewsets.GenericViewSet):
    """
    User Viewset
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None
    permission_classes = [IsAdminUser]
    

    def get_object(self, pk):
        """
        Get Object
        This method is used to get an object from the database.
        """
        return get_object_or_404(self.model, pk=pk)
    
    def get_queryset(self):
        """
        Get Queryset
        This method is used to get a queryset from the database.
        """
        if self.queryset is None:
            self.queryset = self.model.objects\
                .filter(is_active=True)\
                .values('id', 'email', 'name', 'last_name')
        return self.queryset

    @extend_schema(
        request=RequestUserSerializer,
        responses={
            200: OpenApiResponse(description="Successful Response", response=ResponseUserSerializer),
            400: OpenApiResponse(description="Bad Request. User with this email already exists"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not Found"),
        }
    )
    def create(self, request):

        """
        Create
        This method is used to create a new user.
        """
        user_exploitation_id = request.data.get('exploitation', 0)
        user_serializer = self.serializer_class(data=request.data['user'])
        if user_serializer.is_valid():
            user_serializer.save()
            user_exploitation = ExploitationUserSerializer(data={'user': user_serializer.data['id'], 'exploitation': user_exploitation_id})
            user_exploitation.is_valid(raise_exception=True)

            user_exploitation.save()
            return Response({
                'message': 'Usuario registrado correctamente.',
                'user': user_serializer.data,
                'exploitation': user_exploitation.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Hay errores en el registro',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve
        This method is used to retrieve a user.
        """
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        exploitation_exists = ExploitationUser.objects.get(user=user.id)
        return Response({
            "user": user_serializer.data,
            "exploitation": exploitation_exists.exploitation,
            }, status=status.HTTP_200_OK)

    def list(self, request):
        """
        List
        This method is used to list all the users.
        """
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Destroy
        This method is used to destroy a user.
        """
        user_destroy = self.model.objects.filter(id=pk)
        user_destroy = user_destroy.delete()
        if user_destroy[0] > 0:
            return Response({
                'message': 'Usuario eliminado correctamente'
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            'message': 'No existe el usuario que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)

class UserViewSet(viewsets.GenericViewSet):
    """
    User Viewset
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None

    def get_object(self, pk):
        """
        Get Object
        This method is used to get an object from the database.
        """
        return get_object_or_404(self.model, pk=pk)
    
    def get_queryset(self):
        """
        Get Queryset
        This method is used to get a queryset from the database.
        """
        if self.queryset is None:
            self.queryset = self.model.objects\
                .filter(is_active=True)\
                .values('id', 'email', 'name', 'last_name')
        return self.queryset

    def retrieve(self, request, pk=None):
        """
        Retrieve
        This method is used to retrieve a user.
        """
        if self.request.user.id != int(pk):
            return Response({
                'message': 'No tiene permisos para realizar esta operación'  
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        exploitation_exists = ExploitationUser.objects.get(user=user.id)
        return Response({
            "user": user_serializer.data,
            "exploitation": exploitation_exists.exploitation,
            }, status=status.HTTP_200_OK)

    # def create(self, request):
    #     """
    #     Create
    #     This method is used to create a new user.
    #     """
    #     user_exploitation_id = request.data.get('exploitation', 0)
    #     user_serializer = self.serializer_class(data=request.data['user'])
    #     if user_serializer.is_valid():
    #         user_serializer.save()
    #         user_exploitation = ExploitationUserSerializer(data={'user': user_serializer.data['id'], 'exploitation': user_exploitation_id})
    #         user_exploitation.is_valid(raise_exception=True)

    #         user_exploitation.save()
    #         return Response({
    #             'message': 'Usuario registrado correctamente.',
    #             'user': user_serializer.data,
    #             'exploitation': user_exploitation.data
    #         }, status=status.HTTP_201_CREATED)
    #     return Response({
    #         'message': 'Hay errores en el registro',
    #         'errors': user_serializer.errors
    #     }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update
        This method is used to update a user.
        """
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario actualizado correctamente',
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la actualización',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    
    # def destroy(self, request, pk=None):
    #     """
    #     Destroy
    #     This method is used to destroy a user.
    #     """
    #     user_destroy = self.model.objects.filter(id=pk)
    #     user_destroy = user_destroy.delete()
    #     if user_destroy[0] > 0:
    #         return Response({
    #             'message': 'Usuario eliminado correctamente'
    #         }, status=status.HTTP_204_NO_CONTENT)
    #     return Response({
    #         'message': 'No existe el usuario que desea eliminar'
    #     }, status=status.HTTP_404_NOT_FOUND)

    
    