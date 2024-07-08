"""
Serializers
This file contains the serializers of users.
"""
import apps.transactions.api.serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import ExploitationUser, User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer
    This class provides methods for validating and creating a new token pair.
    """
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Custom User Serializer
    This class provides methods for serializing and deserializing a CustomUser.
    """
    class Meta:
        """
        Meta Class
        This class provides the metadata for the serializer.
        """
        model = User
        fields = ('email','name','last_name')

class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    This class provides methods for creating, reading, updating, and deleting users.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        max_length=128,
        style={'input_type': 'password'}
    )
    class Meta:
        """
        Meta Class
        This class provides the metadata for the serializer.
        """
        model = User
        fields = '__all__'
    def create(self,validated_data):
        """
        This method is used to create a new user
        """
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
class UpdateUserSerializer(serializers.ModelSerializer):
    """ 
    Update User Serializer
    This class provides methods for updating a user.
    """
    class Meta:
        """
        Meta Class
        This class provides the metadata for the serializer.
        """
        model = User
        fields = ('email', 'name', 'last_name')

class PasswordSerializer(serializers.Serializer):
    """
    Password Serializer
    This class provides method for validating and creating a new password.
    """
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)
    def validate(self, data):
        """
        validate method
        This method is used to validate the password.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'Error':'Debe ingresar ambas contraseñas iguales'}
            )
        return data

class UserListSerializer(serializers.ModelSerializer):
    """ 
    User List Serializer    
    This class provides method to_representation a user instance.
    """
    class Meta:
        """
        Class Meta
        This class provides the metadata for the serializer.
        """
        model = User

    def to_representation(self, instance):
        """
        to_representation method
        This method is used to represent a user instance.
        """
        return {
            'id': instance['id'],
            'name': instance['name'],
            'last_name': instance['last_name'],
            'email': instance['email'],
            
        }
class ExploitationUserSerializer(serializers.ModelSerializer):
    """
    Exploitation User Serializer
    """
    class Meta:
        """
        Meta Class
        This class provides the metadata for the class serializer ExploitationUser.
        """
        model = ExploitationUser
        fields = '__all__'
class RequestUserSerializer(serializers.Serializer):
    """
    Request User Serializer
    """
    user=UserSerializer()
    exploitation=serializers.IntegerField()

class ResponseUserSerializer(serializers.Serializer):
    """
    Response User Serializer
    """
    user=UserSerializer()
    exploitation=ExploitationUserSerializer()
    
    class Meta:
        """
        Meta Class
        This class provides the metadata for the class serializer ResponseUser.
        """
        model = User
        fields = '__all__'