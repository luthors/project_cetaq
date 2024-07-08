from django.db import models
from simple_history.models import HistoricalRecords 
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from apps.transactions.api.models import Meteo
class UserManager(BaseUserManager):
    """
        User Manager
        Abstract Base Class for managing users.
        This class provides methods for creating, reading, updating, and deleting users.
    """
    def _create_user(self, email, name,last_name, password, is_staff, is_superuser, **extra_fields):
        """
            This method used a private method that is used to create a new user and save it to the database.
            Args: email, name, last_name, password, is_staff, is_superuser
            Returns: User object
        """
        user = self.model(
            email = email,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, name,last_name, password=None, **extra_fields):
        """
            This method is used to create a new user 
            Args: email, name, last_name, password
            Returns: User instance
        """
        return self._create_user(email, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, email, name,last_name, password=None, **extra_fields):
        """
            This method is used to create a new superuser
            Args: email, name, last_name, password
            Returns: superuser instance
        """
        return self._create_user(email, name,last_name, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
        User Model Definition
        Implements the user model for the application.
    """
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    image = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name', 'last_name']
    def __str__(self):
        return f'{self.name} {self.last_name}'
    

class ExploitationUser(models.Model):
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
     exploitation=models.IntegerField('Exploitation')

     
        
    
    