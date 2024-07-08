import math
from django.core import serializers
import shutil
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.core.files.storage import FileSystemStorage
from apps.transactions.api.processes.fugas.class_fugas import Fugas
from apps.transactions.api.processes.match_sectores.class_match import Match
from apps.transactions.api.processes.rendimiento.class_RH import RH
from apps.transactions.api.serializers import (HydraulicPerformanceSerializer,
    ParametersSerializer, RequestSerializer)

from apps.transactions.api.models import Parameters
from .models import Files
from .serializers import FilesSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiRequest, OpenApiTypes
from drf_spectacular.types import OpenApiTypes


ERROR_HEADER_BODY: dict = {'error': 'Faltan componentes del headers y/o data'}
PATH_DIR_FILE: str = 'rest_api_cetaqua/files/'


class LeaksSearch(APIView):
    """
        View for search leaks
        Parameters: JSON with variables 
        days-analyze: number of days to analyze
        city: city
        number-indicators-simultaneous-anomalous-day: number of indicators simultaneous anomalous day
        file: file
    """
    serie=ParametersSerializer
    @extend_schema(
        parameters=[
            OpenApiParameter(name='City', type=OpenApiTypes.STR, required=True,
                             description="Name of City", location=OpenApiParameter.HEADER),
            OpenApiParameter(name='Analyze-Days', type=OpenApiTypes.INT, required=True,
                             description="Number of days of analyze", location=OpenApiParameter.HEADER),
            OpenApiParameter(name='Indicators-Days', type=OpenApiTypes.INT, required=True,
                             description="Bimester", location=OpenApiParameter.HEADER),
        ],
        request=OpenApiRequest(request=RequestSerializer),
        responses={
            200: OpenApiResponse(description="Successful Response", response=HydraulicPerformanceSerializer),
            400: OpenApiResponse(description=f"Bad Request. The input files do not have the required data/columns. Or {ERROR_HEADER_BODY}",),
            401: OpenApiResponse(description="Unauthorized",),
            404: OpenApiResponse(description="Not Found",),
            415: OpenApiResponse(description="Unsupported Media Type, the format of the file is not supported",),
            422: OpenApiResponse(description="Unprocessable Entity - Columns/fields are missing",),
        }

    )
    def post(self, request):
        # como configurar Parameters personalizados para el drf-yasg?
        """ This function return a json with the result of the search o
        Parameters:
            - self : object
                Instance of the class
            - request : HttpRequest
                Request HTTP

        Returns:
            - Response : json
        """
        if 'City' not in request.headers \
                or 'Indicators-Days' not in request.headers \
                or 'Analyze-Days' not in request.headers \
                or 'File' not in request.data \
                or 'Parameters' not in request.data:
            return Response(ERROR_HEADER_BODY, status=status.HTTP_400_BAD_REQUEST)

        city: str = request.headers['City']
        anomalous_days_indicator: int = int(
            request.headers['Indicators-Days']) or 0
        calculation_days: int = int(request.headers['Analyze-Days']) or 0
        params: dict = request.data['Parameters']
        sector_info_file = request.data['File'] or None

        if len(city) == 0 or city.isspace() \
                or len(params) == 0 or params.isspace() \
                or anomalous_days_indicator == 0 \
                or calculation_days == 0 \
                or sector_info_file is None:
            return Response(ERROR_HEADER_BODY, status=status.HTTP_400_BAD_REQUEST)

        fs = FileSystemStorage()
        sector_info_name = fs.save(None, sector_info_file)

        fugas = Fugas(calculation_days, city,
                      anomalous_days_indicator, params, sector_info_name)
        if len(fugas.errors) > 0:
            fs.delete(sector_info_name)
            return fugas.errors[0]

        salida = fugas.leak_algorithm()
        fs.delete(sector_info_name)

        return Response(salida, status=status.HTTP_200_OK)

class HydraulicPerformance(APIView):
    """ 
    View for calculate the hydraulic performance
    """
    @extend_schema(
        parameters=[
            OpenApiParameter(name='Sector', type=OpenApiTypes.STR, required=True,
                             description="Name of Sector", location=OpenApiParameter.HEADER),
            OpenApiParameter(name='City', type=OpenApiTypes.STR, required=True,
                             description="Name of City", location=OpenApiParameter.HEADER),
            OpenApiParameter(name='Year', type=OpenApiTypes.INT, required=True,
                             description="Year", location=OpenApiParameter.HEADER),
            OpenApiParameter(name='Bimester', type=OpenApiTypes.INT, required=True,
                             description="Bimester", location=OpenApiParameter.HEADER),
        ],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'Suplied': {
                        'type': 'binary',
                        'description': 'Excel File with data of supplied',
                    },
                    'Registered': {
                        'type': 'binary',
                        'description': 'File with data of registered',
                    },
                    'Telelectura': {
                        'type': 'binary',
                        'description': 'File with data of telelectura',
                    },
                },
                # continue helpme please with the response={} in drf-spectacular with a difference json without data or whitout models and without serializars ?
            }
        },
        responses={
            200: OpenApiResponse(description="Successful Response", response=HydraulicPerformanceSerializer),
            400: OpenApiResponse(description=f"Bad Request. The input files do not have the required data/columns. Or {ERROR_HEADER_BODY}",),
            401: OpenApiResponse(description="Unauthorized",),
            404: OpenApiResponse(description="Not Found",),
            415: OpenApiResponse(description="Unsupported Media Type, the format of the file is not supported",),
            422: OpenApiResponse(description="Unprocessable Entity - Columns/fields are missing",),
        }

    )
    def post(self, request):
        """
        Post
        This method is used to calculate the hydraulic performance.
        """
        if "Sector" not in request.headers \
                or "City" not in request.headers \
                or "Year" not in request.headers \
                or "Bimester" not in request.headers \
                or "Supplied" not in request.data \
                or "Registered" not in request.data:
            return Response(ERROR_HEADER_BODY, status=status.HTTP_400_BAD_REQUEST)

        sector: str = request.headers['Sector']
        city: str = request.headers['City']
        year: int = int(request.headers['Year']) or 0
        bimester: int = int(request.headers['Bimester']) or 0
        file_supplied: str = request.data['Supplied']
        file_registered: str = request.data['Registered']
        if "Telelectura" in request.data:
            file_telelectura: str = request.data['Telelectura'] or None
        else:
            file_telelectura = None

        if len(city) == 0 or city.isspace() \
                or len(sector) == 0 or sector.isspace() \
                or year == 0 \
                or bimester == 0 \
                or file_supplied is None \
                or file_registered is None:
            return Response(ERROR_HEADER_BODY, status=status.HTTP_400_BAD_REQUEST)
        fs = FileSystemStorage()
        shutil.rmtree(
            PATH_DIR_FILE+f'performance_hydraulic/data/{city}/suministrado')
        shutil.rmtree(
            PATH_DIR_FILE+f'performance_hydraulic/data/{city}/registrado')
        if file_telelectura is not None:
            shutil.rmtree(
                PATH_DIR_FILE+f'performance_hydraulic/data/{city}/telelectura')
            name_file = f'performance_hydraulic/data/{city}/telelectura/{file_telelectura}'
            file_telelectura_name = fs.save(name_file, file_telelectura)
        else:
            file_telelectura_name = None

        name_file = f'performance_hydraulic/data/{city}/suministrado/{file_supplied}'
        file_suplied_name = fs.save(name_file, file_supplied)
        name_file = f'performance_hydraulic/data/{city}/registrado/{file_registered}'
        file_registered_name = fs.save(name_file, file_registered)

        performance = RH(city, sector, year, bimester)
        if len(performance.errors) > 0:
            fs.delete(file_suplied_name)
            fs.delete(file_registered_name)
            return performance.errors[0]
        performance_output = performance.RH_algorithm(file_suplied_name)

        if type(performance_output) is dict:
            for key, value in performance_output.items():
                if type(value) is float and math.isnan(value):
                    performance_output[key] = 0
                if type(value) is float and math.isinf(value):
                    performance_output[key] = 100

        if len(performance.errors) > 0:
            fs.delete(file_suplied_name)
            fs.delete(file_registered_name)
            return performance.errors[0]
        fs.delete(file_registered_name)
        fs.delete(file_suplied_name)

        if file_telelectura_name is not None:
            fs.delete(file_telelectura_name)
        return Response(performance_output, status=status.HTTP_200_OK)


@extend_schema(
    request= {
        'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'Sectores-File': {
                        'type': 'binary',
                        'description': 'Excel File with data of Sector to analyze',
                    },
                    'Contratos-File': {
                        'type': 'binary',
                        'description': 'Excel File with data of contrats to analyze',
                    },
                    'Acometidas-File': {
                        'type': 'binary',
                        'description': 'Excel File with data of acometidas to analyze',
                    }
                }
        },
                # continue helpme please with the response={} in drf-spectacular with a difference json without data or whitout models and without serializars ?
        
    }
)
class SectorsMacth(APIView):
    """
    View for match sectors
    Arguments:
        acometidas: acometidas
        sectores: sectores
        contratos: contratos
    """

    def post(self, request):
        """
        Post
        This method is used to match sectors.
        """
        if "Acometidas-File" not in request.data \
                or "Sectores-File" not in request.data \
                or "Contratos-File" not in request.data:
            return Response(ERROR_HEADER_BODY, status=status.HTTP_400_BAD_REQUEST)

        if request.data['Acometidas-File'] is None \
                or request.data['Sectores-File'] is None \
                or request.data['Contratos-File'] is None:
            return Response(ERROR_HEADER_BODY, status=status.HTTP_400_BAD_REQUEST)

        fs = FileSystemStorage()

        acometidas_file = request.data['Acometidas-File']
        sectores_file = request.data['Sectores-File']
        contratos_file = request.data['Contratos-File']

        sectores_name = fs.save(None, sectores_file)
        acometidas_name = fs.save(None, acometidas_file)
        contratos_name = fs.save(None, contratos_file)

        acometidas = PATH_DIR_FILE + acometidas_name
        sectores = PATH_DIR_FILE + sectores_name
        contratos = PATH_DIR_FILE + contratos_name

        # Las entradas de la clase son las rutas a los archivos
        comp = Match(contratos, sectores, acometidas)
        if len(comp.errores) > 0:
            fs.delete(acometidas_name)
            fs.delete(sectores_name)
            fs.delete(contratos_name)
            return comp.errores[0]
        # Las salidas del modulo son un dataframe y un diccionario
        df, dic = comp.comprobar_archivos()
        # La clase tiene unas funciones para pasar a csv y a json respectivamente
        comp.dataframe_to_csv(
            df, "rest_api_cetaqua/files/store/file/output.csv")
        comp.dict_to_json(
            dic, "rest_api_cetaqua/files/store/file/porcentajes.json")
        fs.delete(acometidas_name)
        fs.delete(sectores_name)
        fs.delete(contratos_name)

        return Response({"percentajes": dic, "message": "Calculo realizado con exito, archivos generados"}, status=status.HTTP_200_OK)


class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    model = Files
