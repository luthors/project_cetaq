
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.users.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('apps.users.api.routers')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('api/',include('apps.transactions.api.routers')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_successful.html'), name='password_reset_complete'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
