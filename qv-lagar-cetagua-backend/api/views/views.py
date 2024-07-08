from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.core.domain.interfaces.anomaly_fillter_full.models import AnomalyFilterFull
from api.core.domain.models.exploitation.models import Exploitation
from api.core.domain.models.hp_expected_variables.models import HPExpectedVariables
from api.core.domain.models.hp_variables.models import HPVariables
from api.core.domain.models.hydraulic_performance.models import HydraulicPerformance
from api.core.domain.models.sector.models import Sector
from api.core.domain.models.anomaly_filter.models import AnomalyFilter
from api.core.domain.models.indicator.models import Indicator
from api.core.domain.models.indicator_threshold.models import IndicatorThreshold
from api.core.domain.models.map.models import Map
from api.serializers.serializers import ExploitationSerializer, HPExpectedVariablesSerializer, SectorSerializer, AnomalyFilterSerializer, IndicatorSerializer, IndicatorThresholdSerializer, MapSerializer, HydraulicPerformanceSerializer, HPVariablesSerializer, HPExpectedVariables
from api.config.default_values_config import A_F_DEFAULT_VALUES_TOLERANCE_LOW, A_F_DEFAULT_VALUES_TOLERANCE_MID, A_F_DEFAULT_VALUES_TOLERANCE_HIGH

class ExploitationViewSet(viewsets.ModelViewSet):
    """
    path url allowed the following methods: GET, POST, PUT for Exploitation model
    
    
    Exploitation View
    This view allows the get, post, and put for Exploitation model
    """
    queryset = Exploitation.objects.all()
    serializer_class = ExploitationSerializer
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        return Exploitation.objects.all()


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer  # crud completo


class IndicatorThresholdViewSet(viewsets.ModelViewSet):
    queryset = IndicatorThreshold.objects.all()
    serializer_class = IndicatorThresholdSerializer

    @action(detail=True, methods=['get'])
    def find_indicator_threshold_by_sector_id_and_tolerance(self, request, pk):
        sector_id = pk
        query= self.request.query_params
        try:
            anomaly_filter_id = AnomalyFilter.objects.filter(
                sector=sector_id).filter( tolerance=query['tolerance'].upper()).first().id
        except:
            anomaly_filter_id = 125
            
        indicator_thresholds = IndicatorThreshold.objects.filter(
            anomaly_filter=anomaly_filter_id)
        # indicator_threshold = IndicatorThresholdSerializer(indicator_thresholds, many=True).data
        anomaly_filter_full = {}
        for indicator_threshold in indicator_thresholds:
            indicator_name = Indicator.objects.get(
                id=indicator_threshold.indicator.id).name

            indicator_threshold_dict = {}
            for key in indicator_threshold.__dict__:
                if key == '_state' or key == 'id' or key == 'created_at' or key == 'updated_at' or key == 'indicator_id' or key == 'anomaly_filter_id':
                    continue
                elif key == 'anomaly_filter':
                    continue
                else:
                    if indicator_threshold.__dict__[key] != None:
                        indicator_threshold_dict[key] = indicator_threshold.__dict__[
                            key]
                        anomaly_filter_full[indicator_name] = indicator_threshold_dict
        return Response(anomaly_filter_full)

class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class AnomalyFilterViewSet(viewsets.ModelViewSet):
    queryset = AnomalyFilter.objects.all()
    serializer_class = AnomalyFilterSerializer

    @parser_classes([JSONParser])
    def create(self, request, *args, **kwargs):
        new_anomaly_filter_instance = request.data['anomaly_filter']
        map_sector = new_anomaly_filter_instance['sector']
        tolerance_anml = new_anomaly_filter_instance['tolerance']
        existing_anomaly_filter = AnomalyFilter.objects.filter(sector=map_sector).filter(tolerance=tolerance_anml).first()
        if existing_anomaly_filter:
            updated_anomaly_filter = AnomalyFilterSerializer(
                existing_anomaly_filter, data=new_anomaly_filter_instance)
            updated_anomaly_filter.is_valid(raise_exception=True)
            updated_anomaly_filter.save()
            json_anomaly_filter_full = request.data['anomaly_filter_full']
            for indicator_json in json_anomaly_filter_full:
                indicator_id = Indicator.objects.filter(
                    name=indicator_json).first().id
                anomaly_filter_id = updated_anomaly_filter.data['id']
                existing_indicator_threshold = IndicatorThreshold.objects.filter(
                    indicator=indicator_id, anomaly_filter=anomaly_filter_id).first()
                if existing_indicator_threshold:
                    indicator_threshold_data = json_anomaly_filter_full[indicator_json]
                    indicator_threshold_data['indicator'] = indicator_id
                    indicator_threshold_data['anomaly_filter'] = anomaly_filter_id
                    updated_indicator_threshold = IndicatorThresholdSerializer(
                        existing_indicator_threshold, data=indicator_threshold_data)
                    updated_indicator_threshold.is_valid(raise_exception=True)
                    updated_indicator_threshold.save()
                else:
                    indicator_threshold_data = json_anomaly_filter_full[indicator_json]
                    indicator_threshold_data['indicator'] = indicator_id
                    indicator_threshold_data['anomaly_filter'] = anomaly_filter_id
                    new_indicator_threshold = IndicatorThresholdSerializer(
                        data=indicator_threshold_data)
                    new_indicator_threshold.is_valid(raise_exception=True)
                    new_indicator_threshold.save()
            return Response({'anomaly_filter': updated_anomaly_filter.data, 'anomaly_filter_full': json_anomaly_filter_full}, status=status.HTTP_200_OK)
        else:
            new_anomaly_filter_instance = AnomalyFilterSerializer(
                data=new_anomaly_filter_instance)
            new_anomaly_filter_instance.is_valid(raise_exception=True)
            new_anomaly_filter_instance.save()
            json_anomaly_filter_full = request.data['anomaly_filter_full']
            for indicator_json in json_anomaly_filter_full:
                indicator_id = Indicator.objects.filter(
                    name=indicator_json).first().id
                anomaly_filter_id = new_anomaly_filter_instance.data['id']
                existing_indicator_threshold = IndicatorThreshold.objects.filter(
                    indicator=indicator_id, anomaly_filter=anomaly_filter_id).first()
                indicator_threshold_data = json_anomaly_filter_full[indicator_json]
                indicator_threshold_data['indicator'] = indicator_id
                indicator_threshold_data['anomaly_filter'] = anomaly_filter_id
                new_indicator_threshold = IndicatorThresholdSerializer(
                    data=indicator_threshold_data)
                new_indicator_threshold.is_valid(raise_exception=True)
                new_indicator_threshold.save()
            return Response({'anomaly_filter': new_anomaly_filter_instance.data, 'anomaly_filter_full': json_anomaly_filter_full}, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['get'])
    def find_anomaly_filter_by_sector_id_and_tolerance(self, request, pk):
        sector_id = pk
        query= self.request.query_params
        anomaly_filters = AnomalyFilter.objects.filter(sector=sector_id).filter( tolerance=query['tolerance'].upper())
        if not anomaly_filters:
            return Response({'error': 'Anomaly filter not found'}, status=404)
        return Response(AnomalyFilterSerializer(anomaly_filters, many=True).data)

    # http://127.0.0.1:8081/api/filtros_anomalias/fill_indicators/
    # con este endpoint y la función fill_indicators se cargan los indicadores
    @action(detail=False, methods=['POST'])
    def fill_indicators(self, request, *args, **kwargs):
        existing_indicators = Indicator.objects.all()
        if existing_indicators:
            return Response({'error': 'Indicators already exists'}, status=status.HTTP_409_CONFLICT)
        else:
            indicator_data = request.data['anomaly_filter_full']
            for indicator in indicator_data:
                indicator = {
                    'name': indicator,
                    'description': 'Indicator '+indicator,
                }
                new_indicator_instance = IndicatorSerializer(data=indicator)
                new_indicator_instance.is_valid(raise_exception=True)
                new_indicator_instance.save()
            return Response(new_indicator_instance.data, status=status.HTTP_201_CREATED)


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    @action(detail=False, methods=['post'])
    @parser_classes([JSONParser])
    def create_map(self, request, *args, **kwargs):
        map = self.get_serializer(data=request.data)
        map.is_valid(raise_exception=True)
        existing_map = Map.objects.filter(name=request.data['name']).first()

        if existing_map:
            return Response(map.errors, status=status.HTTP_409_CONFLICT)
        else:
            map.save()
            headers = self.get_success_headers(map.data)
            # self.perform_create(map)
            sectores = request.data['geojson']['features']
            for elemento in sectores:
                sector = {
                    'name': elemento['properties']['Name'],
                    'description': 'Sector '+elemento['properties']['Name'],
                    'map': map.data['id'],
                }
                new_sector_instance = SectorSerializer(data=sector)
                new_sector_instance.is_valid(raise_exception=True)
                new_sector_instance.save()
                sector_id = int(new_sector_instance.data['id'])
                map_id = int(map.data['id'])
                request.data['anomaly_filter']['map'] = map_id
                request.data['anomaly_filter']['sector'] = sector_id
                anomaly_filter_viewset = AnomalyFilterViewSet()
                
                request.data['anomaly_filter']= A_F_DEFAULT_VALUES_TOLERANCE_LOW['anomaly_filter'];
                request.data['anomaly_filter_full']= A_F_DEFAULT_VALUES_TOLERANCE_LOW['anomaly_filter_full'];
                request.data['anomaly_filter']['map'] = map_id
                request.data['anomaly_filter']['sector'] = sector_id
                response=anomaly_filter_viewset.create(request)
                
                request.data['anomaly_filter']= A_F_DEFAULT_VALUES_TOLERANCE_MID['anomaly_filter'];
                request.data['anomaly_filter_full']= A_F_DEFAULT_VALUES_TOLERANCE_MID['anomaly_filter_full'];
                request.data['anomaly_filter']['map'] = map_id
                request.data['anomaly_filter']['sector'] = sector_id
                response=anomaly_filter_viewset.create(request)
                
                request.data['anomaly_filter']= A_F_DEFAULT_VALUES_TOLERANCE_HIGH['anomaly_filter'];
                request.data['anomaly_filter_full']= A_F_DEFAULT_VALUES_TOLERANCE_HIGH['anomaly_filter_full'];
                request.data['anomaly_filter']['map'] = map_id
                request.data['anomaly_filter']['sector'] = sector_id
                response=anomaly_filter_viewset.create(request)
                    
            return Response(map.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def find_sector_on_map(self, request, pk):
        map_id = pk
        sectors = Sector.objects.filter(map_id=map_id)
        return Response(SectorSerializer(sectors, many=True).data)


class HPExpectedVariablesViewSet(viewsets.ModelViewSet):
    queryset = HPExpectedVariables.objects.all()
    serializer_class = HPExpectedVariablesSerializer

class HPVariablesViewSet(viewsets.ModelViewSet):
    queryset = HPVariables.objects.all()
    serializer_class = HPVariablesSerializer
    
class HydraulicPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HydraulicPerformance.objects.all()
    serializer_class = HydraulicPerformanceSerializer
    @action(detail=False, methods=['get'])
    def find_hydraulic_performance_by_sector_id_and_year_and_bimester(self, request):
        sector_id = request.query_params['sector']
        year = request.query_params['year']
        bimester = request.query_params['bimester']
        found_hydraulic_performances = HydraulicPerformance.objects.filter(sector=sector_id).filter(year=year).filter(bimester=bimester).first()
        if not found_hydraulic_performances:
            return Response({'error': 'Hydraulic performance not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(HydraulicPerformanceSerializer(found_hydraulic_performances, many=False).data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['post'])
    def create_hydraulic_performance(self, request, *args, **kwargs):
        sector_id = request.data['sector']
        year = request.data['year']
        bimester = request.data['bimester']
        hydraulic_performance_most_recent = HydraulicPerformance.objects.filter(sector=sector_id).order_by('-year', '-bimester').first()
        existing_hydraulic_performance = HydraulicPerformance.objects.filter(sector=sector_id).filter(year=year).filter(bimester=bimester).first()
        if existing_hydraulic_performance:
            return Response({'error': 'Hydraulic performance already exists'}, status=409)
        else:
            hydraulic_performance = self.get_serializer(data=request.data)
            hydraulic_performance.is_valid(raise_exception=True)
            hydraulic_performance.save()
            hp_variables = request.data['hp_variables']
            hp_expected_variables = request.data['hp_expected_variables']
            HPVariables.objects.create(hydraulic_performance_id=hydraulic_performance.data['id'], **hp_variables)
            if not hydraulic_performance_most_recent:
                HPExpectedVariables.objects.create(hydraulic_performance_id=hydraulic_performance.data['id'], **hp_expected_variables)       
            else:
                if hydraulic_performance_most_recent.year < year or (hydraulic_performance_most_recent.year == year and hydraulic_performance_most_recent.bimester < bimester):
                    is_most_recent = True
                else:
                    is_most_recent = False
                hp_expected_variables_existing=HPExpectedVariables.objects.filter(hydraulic_performance_id=hydraulic_performance_most_recent).first()
                if hp_expected_variables_existing and is_most_recent:
                    hp_expected_variables_existing.delete()
                    HPExpectedVariables.objects.create(hydraulic_performance_id=hydraulic_performance.data['id'], **hp_expected_variables)
            return Response(hydraulic_performance.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def find_hydraulic_performance_by_sector_id(self, request, pk):
        sector_id = pk
        found_hydraulic_performances = HydraulicPerformance.objects.filter(sector=sector_id).all().order_by('year', 'bimester')
        hp_variables_list=[]
        hp_expected_variables_unique = None
        
        for found_hydraulic_performance in found_hydraulic_performances:
            hp_variables=HPVariables.objects.filter(hydraulic_performance_id=found_hydraulic_performance.id).first()
            hp_expected_variables_unique=HPExpectedVariables.objects.filter(hydraulic_performance_id=found_hydraulic_performance.id).first()
            hp_variables_list.append(hp_variables)
            
        hp_variables_response=HPVariablesSerializer(hp_variables_list, many=True).data
        hp_expected_variables_response=HPExpectedVariablesSerializer(hp_expected_variables_unique).data
        hydraulic_response = HydraulicPerformanceSerializer(found_hydraulic_performances, many=True).data
        response=[hydraulic_response] + [hp_variables_response] + [hp_expected_variables_response]
        return Response(response, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_hydraulic_performance_by_id(self, request, pk):
        hp_id = pk
        found_hydraulic_performance = HydraulicPerformance.objects.filter(id=hp_id).first()
        if not found_hydraulic_performance:
            return Response({'error': 'Hydraulic performance not found'}, status=status.HTTP_404_NOT_FOUND)
        found_hp_variables = HPVariables.objects.filter(hydraulic_performance_id=hp_id).first()
        # found_hp_expected_variables = HPExpectedVariables.objects.filter(hydraulic_performance_id=hp_id).first()
        
        found_hydraulic_performance.delete()
        found_hp_variables.delete()
        # found_hp_expected_variables.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    