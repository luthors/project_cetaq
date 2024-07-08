from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.api.serializers import CustomTokenObtainPairSerializer, CustomUserSerializer
from rest_api_cetaqua.settings.base import BASE_DIR
from apps.users.models import ExploitationUser, User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

class LoginView(TokenObtainPairView):
    """
    Login
    This class provides methods for logging in a user.
    """
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        """
        Post
        This method is used to login a user.
        """
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(
            request=request,
            username=email,
            password=password
        )
        if user:
            login_serializer = self.serializer_class(data=request.data)
            user_db= User.objects.get(id=user.id)
            
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                exploitation_exists=1
                if not user_db.is_superuser:
                    exploitation_exists = ExploitationUser.objects.get(user=user.id).exploitation
                user_serializer_data = user_serializer.data
                user_serializer_data['id'] = user.id
                
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer_data,
                    'exploitation': exploitation_exists,
                    'message': 'Inicio de Sesion Existoso',
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(GenericAPIView):
    """
    Logout
    This class provides methods for logout a user.
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        """
        Post
        This method is used to logout a user.
        """
        try:
            token = RefreshToken().for_user(request.user)
            token.blacklist()
            logout(request)
            return Response({'message': 'The user successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        