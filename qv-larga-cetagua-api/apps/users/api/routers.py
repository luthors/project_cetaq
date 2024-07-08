"""
Routers
This file contains the routers of users and set_password for the API
"""
from rest_framework.routers import DefaultRouter
from apps.users.api.api import UserViewSet, UserPasswordViewSet, UserViewAdminSet
router = DefaultRouter()
router.register('user', UserViewSet, basename="users")
router.register('admin', UserViewAdminSet, basename="users_admin")
router.register('', UserPasswordViewSet, basename="set_password")
urlpatterns = router.urls