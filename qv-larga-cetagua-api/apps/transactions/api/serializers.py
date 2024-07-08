from apps.transactions.api.models import Parameters
from rest_framework import serializers
from .models import Flow, Meteo, DailyVolume, MinFlow, MinFlowDivmeanFlow, MinFlowMultmeanFlow, Pressure

class FlowSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    meanWeekDays = serializers.IntegerField()
    hours = serializers.IntegerField()
    tolerance = serializers.FloatField()
    
    class Meta:
        model = Flow
        fields = '__all__'
    
class MeteoSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    movingAverageDays = serializers.IntegerField()
    fixedAverageDays= serializers.IntegerField()
    weightAverage= serializers.IntegerField()
    weightDeviation= serializers.FloatField()
    tolerance= serializers.FloatField()
    class Meta:
        model = Meteo
        fields = '__all__'
class MinFlowSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    movingAverageDays = serializers.IntegerField()
    fixedAverageDays= serializers.IntegerField()
    weightAverage= serializers.IntegerField()
    weightDeviation= serializers.FloatField()
    tolerance= serializers.FloatField()
    
    class Meta:
        model = MinFlow
        fields = '__all__'

class MinFlowDivmeanFlowSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    movingAverageDays = serializers.IntegerField()
    fixedAverageDays= serializers.IntegerField()
    weightAverage= serializers.IntegerField()
    weightDeviation= serializers.FloatField()
    tolerance= serializers.FloatField()
    class Meta:
        model = MinFlowDivmeanFlow
        fields = '__all__'

class MinFlowMultmeanFlowSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    movingAverageDays = serializers.IntegerField()
    fixedAverageDays= serializers.IntegerField()
    weightAverage= serializers.IntegerField()
    weightDeviation= serializers.FloatField()
    tolerance= serializers.FloatField()
    class Meta:
        model = MinFlowMultmeanFlow
        fields = '__all__'
class PressureSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    movingAverageDays = serializers.IntegerField()
    weightAverage= serializers.IntegerField()
    weightDeviation= serializers.FloatField()
    class Meta:
        model = Pressure
        fields = '__all__'
        
class DailyVolumeSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    movingAverageDays = serializers.IntegerField()
    fixedAverageDays= serializers.IntegerField()
    weightAverage= serializers.IntegerField()
    weightDeviation= serializers.FloatField()
    tolerance= serializers.FloatField()
       
    class Meta:
        model = DailyVolume
        fields = '__all__'
class MinFlowSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    movingAverageDays = serializers.IntegerField()
    fixedAverageDays= serializers.IntegerField()
    weightAverage= serializers.IntegerField()
    weightDeviation= serializers.FloatField()
    tolerance= serializers.FloatField()
    
    class Meta:
        model = MinFlow
        fields = '__all__'
        
class ParametersSerializer(serializers.Serializer):
    flow = FlowSerializer()
    minFlow = MinFlowSerializer()
    dailyVolume = DailyVolumeSerializer()
    pressure = PressureSerializer()
    minFlowMultmeanFlow = MinFlowMultmeanFlowSerializer()
    minFlowDivmeanFlow = MinFlowDivmeanFlowSerializer()
    meteo = MeteoSerializer()
    
    class Meta:
        model = Parameters
        fields = '__all__'
        
class RequestSerializer(serializers.Serializer):
    File = serializers.FileField()
    parameters = ParametersSerializer()
    class Meta:
        model = Parameters
        fields = '__all__'

class HydraulicPerformanceSerializer(serializers.Serializer):
    sector = serializers.CharField()
    year = serializers.IntegerField()
    bimester = serializers.IntegerField()
    contracts_number = serializers.IntegerField()
    registered_liters = serializers.FloatField()
    adjusted_liters = serializers.FloatField()
    reading_liters = serializers.FloatField()
    billed_liters = serializers.FloatField()
    supplied_liters = serializers.FloatField()
    registered_percentage = serializers.FloatField()
    adjusted_percentage = serializers.FloatField()
    reading_percentage = serializers.FloatField()
    total_percentage = serializers.FloatField()
    expected_supplied = serializers.FloatField()
    expected_registered = serializers.FloatField()
    expected_RH = serializers.FloatField()
