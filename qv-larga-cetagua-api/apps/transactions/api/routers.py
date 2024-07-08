from django.urls import path, include

from apps.transactions.views import HydraulicPerformance, LeaksSearch, SectorsMacth, FilesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')

urlpatterns = [
    path('leaks_search/', LeaksSearch.as_view(), name='leaks_search'),
    path('hydraulic_performance/', HydraulicPerformance.as_view(), name='hydraulic_performance'),
    path('sectors_match/', SectorsMacth.as_view(), name='sectors_match'),
    path('', include(router.urls))
]