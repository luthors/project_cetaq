from rest_framework import serializers
from api.core.domain.models.anomaly_filter.models import AnomalyFilter
from api.core.domain.models.exploitation.models import Exploitation
from api.core.domain.models.indicator.models import Indicator
from api.core.domain.models.indicator_threshold.models import IndicatorThreshold
from api.core.domain.models.sector.models import Sector
from api.core.domain.models.map.models import Map
from api.core.domain.models.hydraulic_performance.models import HydraulicPerformance
from api.core.domain.models.hp_expected_variables.models import HPExpectedVariables
from api.core.domain.models.hp_variables.models import HPVariables

class ExploitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exploitation
        fields = '__all__'
        
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'
        
class IndicatorThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorThreshold
        fields = '__all__'

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'

class AnomalyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyFilter
        fields = '__all__'
        
class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'

class HydraulicPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydraulicPerformance
        fields = '__all__'

class HPExpectedVariablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HPExpectedVariables
        fields = '__all__'

class HPVariablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HPVariables
        fields = '__all__'