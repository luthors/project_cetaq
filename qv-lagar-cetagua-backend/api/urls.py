from django.urls import path, include
from rest_framework import routers
from api.views import views

router = routers.DefaultRouter()
router.register(r'exploitation', views.ExploitationViewSet)
router.register(r'sector', views.SectorViewSet)
router.register(r'indicator_threshold', views.IndicatorThresholdViewSet)
router.register(r'indicador', views.IndicatorViewSet)
router.register(r'anomaly_filter', views.AnomalyFilterViewSet)
router.register(r'map', views.MapViewSet)
router.register(r'hydraulic_performance', views.HydraulicPerformanceViewSet)
router.register(r'hp_expected_variables', views.HPExpectedVariablesViewSet)
router.register(r'hp_variables', views.HPVariablesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]