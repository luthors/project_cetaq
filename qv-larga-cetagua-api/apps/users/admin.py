from django.contrib import admin
from apps.users.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AuthenticationForm

# class CustomAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = User

# class CustomUserAdmin(UserAdmin):
#     # Personalizaciones adicionales si es necesario
#     list_display = ('email', 'name', 'last_name', 'is_active', 'is_staff')
#     ordering = ('email',)
    
#     # Declaración explícita de fieldsets sin 'username' o 'first_name'
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('name', 'last_name')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

# admin.site.register(User, CustomUserAdmin)
admin.site.register(User)
# admin.site.login_form = CustomAuthenticationForm

