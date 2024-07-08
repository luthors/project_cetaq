from rest_framework.response import Response
import json
from apps.transactions.api.processes.fugas import get_data_Lagar as data_Lagar
from apps.transactions.api.processes.fugas import indicadores_Lagar as indicadores
import pandas as pd

class Fugas:
    
    def __init__(self, calculation_days:int, city:str, num_indicadores:int, parameters:dict, file_sector_info:str, errors:list = []):
        '''
        Initialize and get the data to make the leak calculus.

        Parameters
        ----------
        calculation_self.calculation_days : int
            Number of previous self.calculation_days to make the calculus.
        city : str
            Name of the city in which to use the algorithm.

        '''
        self.errors=[]
        self.data = data_Lagar.get_data_sector(file_sector_info)      
        if type(self.data) is Response: 
            if self.data.data is not None:
                self.errors.append(self.data)
                return None
        
        self.input_param = data_Lagar.get_data_param(json.loads(parameters))
        if type(self.input_param) is Response:
            if self.input_param.data is not None:
                self.errors.append(self.input_param)
                return None
        # self.input_param is loaded from request and converted of json to dict
        # self.input_param = data_Lagar.get_data_param('apps/transactions/api/processes/fugas/datos/input_param.json')
        self.calculation_days = calculation_days
        self.city = city
        self.num_indicadores = num_indicadores
        
    def leak_algorithm(self):
        self.output_data = {
            'flow': {
                },
            'minFlow': {
                },
            'dailyVolume': {
                },
            'pressure': {
                },
            'minFlowMultmeanFlow': {
                },
            'minFlowDivmeanFlow': {
                },
            'meteo': {
                },
            'AnomalousDays': {
                }
            }

        analizar_envolvente = self.input_param['flow']['active']
        analizar_caudal = self.input_param['minFlow']['active']
        analizar_volumen = self.input_param['dailyVolume']['active']
        analizar_presion = self.input_param['pressure']['active']
        analizar_producto = self.input_param['minFlowMultmeanFlow']['active']
        analizar_ratio = self.input_param['minFlowDivmeanFlow']['active']
        
        incluir_meteo = self.input_param['meteo']['active']
        
        activos = []

        if analizar_envolvente:
            activos += ['flow']
            
            self.output_data['flow']['data'], self.output_data['flow']['datetime'], self.output_data['flow']['anomaly'], self.output_data['flow']['meanSurrounding'] = indicadores.ind_envolvente(pd.Series(self.data.Caudal.interpolate(), name='Envolvente Caudal'), self.calculation_days, self.input_param['flow']['meanWeekDays'], self.input_param['flow']['hours'], self.input_param['flow']['tolerance'])

        if analizar_caudal:
            activos += ['minFlow']

            self.output_data['minFlow']['data'], self.output_data['minFlow']['datetime'], self.output_data['minFlow']['anomaly'] = indicadores.ind_medias(self.data.Caudal.resample('D').mean(), self.calculation_days, self.input_param['minFlow']['movingAverageDays'], self.input_param['minFlow']['weightAverage'], self.input_param['minFlow']['weightDeviation'], True, self.input_param['minFlow']['fixedAverageDays'], self.input_param['minFlow']['tolerance'])

        if analizar_volumen:
            activos += ['dailyVolume']

            self.output_data['dailyVolume']['data'], self.output_data['dailyVolume']['datetime'], self.output_data['dailyVolume']['anomaly'] = indicadores.ind_medias(self.data.Volumen.resample('D').mean(), self.calculation_days, self.input_param['dailyVolume']['movingAverageDays'], self.input_param['dailyVolume']['weightAverage'], self.input_param['dailyVolume']['weightDeviation'], True, self.input_param['dailyVolume']['fixedAverageDays'], self.input_param['dailyVolume']['tolerance'])

        if analizar_presion:
            activos += ['pressure']

            self.output_data['pressure']['data'], self.output_data['pressure']['datetime'], self.output_data['pressure']['anomaly'] = indicadores.ind_medias(self.data.Presion.resample('D').mean(), self.calculation_days, self.input_param['pressure']['movingAverageDays'], self.input_param['pressure']['weightAverage'], self.input_param['pressure']['weightDeviation'], media_fija = False)
         
        if analizar_producto:
            activos += ['minFlowMultmeanFlow']

            self.output_data['minFlowMultmeanFlow']['data'], self.output_data['minFlowMultmeanFlow']['datetime'], self.output_data['minFlowMultmeanFlow']['anomaly'] = indicadores.ind_medias(pd.Series(self.data.Caudal.resample('D').mean() * self.data.Caudal.resample('D').min(), name='Cmin*Cmean'), self.calculation_days, self.input_param['minFlowMultmeanFlow']['movingAverageDays'], self.input_param['minFlowMultmeanFlow']['weightAverage'], self.input_param['minFlowMultmeanFlow']['weightDeviation'], media_fija = False)
           
        if analizar_ratio:
            activos += ['minFlowDivmeanFlow']

            self.output_data['minFlowDivmeanFlow']['data'], self.output_data['minFlowDivmeanFlow']['datetime'], self.output_data['minFlowDivmeanFlow']['anomaly'] = indicadores.ind_medias(pd.Series(self.data.Caudal.resample('D').min() / self.data.Caudal.resample('D').mean(), name='Cmin/Cmed'), self.calculation_days, self.input_param['minFlowDivmeanFlow']['movingAverageDays'], self.input_param['minFlowDivmeanFlow']['weightAverage'], self.input_param['minFlowDivmeanFlow']['weightDeviation'], media_fija = False)
        
        anomaly_data = []
        if self.num_indicadores > len(activos):
            self.num_indicadores = len(activos)
            
        for i in range(self.calculation_days):
            ind = 0
            for var in activos:
                if var == 'flow':
                    ind += self.output_data[var]['anomaly'][i*24]
                else:
                    ind += self.output_data[var]['anomaly'][i]
                    anomaly_dates = self.output_data[var]['datetime']
            if ind >= self.num_indicadores:
                anomaly_data += [int(1)]
            else:
                anomaly_data += [int(0)]
                
        self.output_data['AnomalousDays']['datetime'] = anomaly_dates
        self.output_data['AnomalousDays']['anomaly'] = anomaly_data
        
        if incluir_meteo:
            self.output_data['meteo']['datetime'], self.output_data['meteo']['precipitation'], self.output_data['meteo']['temperature'] = self.meteo_data()
        
        return self.output_data
    
    def meteo_data(self): # Modificar parametros, no representamos, esto solo para visualizarlo nosotros
        meteo = data_Lagar.get_data_meteo(self.city, self.calculation_days, self.data.index[-1].date())
        
        return meteo.index.tolist(), meteo.prec.tolist(), meteo.tmed.tolist()
        
        
        
# num_dias_analizar = 7
# ciudad = 'Roquetas de Mar'
# numero_indicadores_simultaneos_dia_anomalo = 1

# fugas = Fugas(num_dias_analizar, ciudad, numero_indicadores_simultaneos_dia_anomalo)
# salida = fugas.leak_algorithm()