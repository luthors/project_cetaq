import os
import requests
import pandas
from datetime import date, timedelta, datetime
import glob

class SAIHInformation:
    
    '''
    Agrupacion : 5(cincominutal), 60(horaria), 1(diaria), 7(semanal), 31(mensual), 100(acumulado)
    
    Provincia: 1(Cádiz), 2(Málaga), 3(Granada), 4(Almería), 5(Huelva)
    '''

    def get_historical_data(self, init : str, agrupation : int, province : int, station : int, sensor : str, fin = datetime.strftime(date.today(), '%d/%m/%Y')) -> int:
        '''
        
        This function makes a SAIH's request and download the desired data
        
        Parameters
        ----------
        init : str
            Start date to download.
        agrupation : int
            Periodicity of the values.
        province : int
            ID of the province.
        station : int
            ID of the station from where to get the values (3 first digits of the sensor code).
        sensor : str
            ID of the sensor from which to get the values.
        fin : TYPE, optional
            End date to download. The default is today's value.

        '''
        init_day = datetime.strptime(init, '%d/%m/%Y').date()
        end_date = datetime.strptime(fin, '%d/%m/%Y').date()
        if sensor[3] == 'P':
            var = 'Precipitation'
        elif sensor[3] == 'M':
            var = 'Temperature'
        elif sensor[3] == 'E':
            var = 'Volume'
        else:
            var = 'Unknown_variable'
        while init_day < end_date - timedelta(days = 31):
            end_day = init_day + timedelta(31)
            url = "http://www.redhidrosurmedioambiente.es/saih/datos/a/la/carta/csv?datepickerini=" + init_day.strftime("%d/%m/%Y") + " 00:00" + "&datepickerfin=" + end_day.strftime("%d/%m/%Y") + " 00:00" + "&agrupacion=" + str(agrupation) + " &subsistema=" + "&provincia=" + str(province) + "&tipoestacion=" + "&estacion=" + str(station) + "&tipo=" + "&sensor=" +  sensor
            resp = requests.get(url)
            output = open(f"{var}_{init_day.strftime('%d_%m_%Y')}.csv", 'wb')
            output.write(resp.content)
            output.close()
            
            init_day = end_day + timedelta(days=1)
        
        end_day = end_date
        url = "http://www.redhidrosurmedioambiente.es/saih/datos/a/la/carta/csv?datepickerini=" + init_day.strftime("%d/%m/%Y") + " 00:00" + "&datepickerfin=" + end_day.strftime("%d/%m/%Y") + " 00:00" + "&agrupacion=" + str(agrupation) + " &subsistema=" + "&provincia=" + str(province) + "&tipoestacion=" + "&estacion=" + str(station) + "&tipo=" + "&sensor=" +  sensor
        resp = requests.get(url)
        output = open(f"{var}_{init_day.strftime('%d_%m_%Y')}.csv", 'wb')
        output.write(resp.content)
        output.close()

    def get_data_last_days (self, province : int, sensor : str, agrupation : int, days: int):
        '''

        Parameters
        ----------
        province : int
            ID of the province.
        sensor : str
            ID of the sensor from which to get the values.
        agrupation : int
            Periodicity of the values.
        days : int
            Number of last days to get the values.

        Returns
        -------
        total_data : pandas.DataFrame
            Returns a DataFrame with the values of the last days.

        '''
        today = date.today()
        init_day = today - timedelta(days = days)
        estacion = int(sensor[:3])
        if sensor[3] == 'P':
            var = 'Precipitation'
            pos = -1
        elif sensor[3] == 'M':
            var = 'Temperature'
            pos = -2
        elif sensor[3] == 'E':
            var = 'Volume'
            pos = -1
        else:
            var = 'Unknown_variable'
            
        if agrupation == 5 or agrupation == 60:
            formato = '%d/%m/%Y %H:%M'
        else:
            formato = '%d/%m/%y'
        self.get_historical_data(init_day.strftime("%d/%m/%Y"), agrupation, province, estacion, sensor)
        
        total_data = pandas.DataFrame()  
        for archivo in glob.glob(os.getcwd()+f'/{var}_*.csv'):
            try:
                data = pandas.read_csv(archivo, sep=';')
            except:
                print('No hay datos disponibles para la peticion requerida')
                os.remove(archivo)
            total_data = pandas.concat([total_data, data])
            os.remove(archivo)
            
        total_data[total_data.columns[pos]] = total_data.iloc[:,pos].replace(",",".", regex= True).astype(float)
        
        total_data.set_index('Fecha', inplace=True)
        try:
            total_data.index = pandas.to_datetime(total_data.index, format=formato)
        except:
            total_data.index = pandas.to_datetime(total_data.index, format='%d/%m/%y %H:%M')
            
        return total_data
    
    def get_data_period (self, province : int, sensor : str, agrupation : int, init : str, fin = datetime.strftime(date.today(), '%d/%m/%Y')):
        '''

        Parameters
        ----------
        province : int
            ID of the province.
        sensor : str
            ID of the sensor from which to get the values.
        agrupation : int
            Periodicity of the values.
        init : str
            Start date to download.
        fin : TYPE, optional
            End date to download. The default is today's value.

        Returns
        -------
        total_data : TYPE
            Returns a DataFrame with the values of the required period.

        '''
        estacion = int(sensor[:3])
        if sensor[3] == 'P':
            var = 'Precipitation'
            pos = -1
        elif sensor[3] == 'M':
            var = 'Temperature'
            pos = -2
        elif sensor[3] == 'E':
            var = 'Volume'
            pos = -1
        else:
            var = 'Unknown_variable'
       
        if agrupation == 5 or agrupation == 60:
            formato = '%d/%m/%Y %H:%M'
        else:
            formato = '%d/%m/%y'
        self.get_historical_data(init, agrupation, province, estacion, sensor, fin)
        
        total_data = pandas.DataFrame()  
        for archivo in glob.glob(os.getcwd()+f'/{var}_*.csv'):
            try:
                data = pandas.read_csv(archivo, sep=';')
            except:
                print('No hay datos disponibles para la peticion requerida')
                os.remove(archivo)
            total_data = pandas.concat([total_data, data])
            os.remove(archivo)
            
        total_data[total_data.columns[pos]] = total_data.iloc[:,pos].replace(",",".", regex= True).astype(float)
        
        total_data.set_index('Fecha', inplace=True)
        try:
            total_data.index = pandas.to_datetime(total_data.index, format=formato)
        except:
            total_data.index = pandas.to_datetime(total_data.index, format='%d/%m/%y %H:%M')
            
        return total_data
    
    def get_csv (self, province : int, sensor : str, agrupation : int, init : str, fin = datetime.strftime(date.today(), '%d/%m/%Y')):
        '''
        This function makes a .csv file with the data of a desired period and save it in '/resultados'
        
        Parameters
        ----------
        province : int
            ID of the province.
        sensor : str
            ID of the sensor from which to get the values.
        agrupation : int
            Periodicity of the values.
        init : str
            Start date to download.
        fin : TYPE, optional
            End date to download. The default is today's value.

        Returns
        -------
        None.

        '''
        estacion = int(sensor[:3])
        if sensor[3] == 'P':
            var = 'Precipitation'
            pos = -1
        elif sensor[3] == 'M':
            var = 'Temperature'
            pos = -2
        elif sensor[3] == 'E':
            var = 'Volume'
            pos = -1
        else:
            var = 'Unknown_variable'
            
        self.get_historical_data(init, agrupation, province, estacion, sensor, fin)
        
        total_data = pandas.DataFrame()  
        for archivo in glob.glob(os.getcwd()+f'/{var}_*.csv'):
            try:
                data = pandas.read_csv(archivo, sep=';')
            except:
                print('No hay datos disponibles para la peticion requerida')
            total_data = pandas.concat([total_data, data])
            os.remove(archivo)            

        total_data[total_data.columns[pos]] = total_data.iloc[:,pos].replace(",",".", regex= True).astype(float)
        try:
          os.stat('resultados')
        except:
          os.mkdir('resultados')
          
        total_data.to_csv(f"resultados/{var}_{init.replace('/','_')}_to_{fin.replace('/','_')}.csv", sep=';', index=False)
            
    def get_acumulado(self, province : int, sensor : str, init : str, fin = datetime.strftime(date.today(), '%d/%m/%Y')):
        '''

        Parameters
        ----------
        province : int
            ID of the province.
        sensor : str
            ID of the sensor from which to get the values.
        init : str
            Start date to download.
        fin : TYPE, optional
            End date to download. The default is today's value.

        Returns
        -------
        Returns the accumulate value of the required param.

        '''
        estacion = int(sensor[:3])
        if sensor[3] == 'P':
            var = 'Precipitation'
            pos = -1
        elif sensor[3] == 'M':
            var = 'Temperature'
            pos = -2
        elif sensor[3] == 'E':
            var = 'Volume'
            pos = -1
        else:
            var = 'Unknown_variable'
        self.get_historical_data(init, 100, province, estacion, sensor, fin)
        
        total_data = pandas.DataFrame()  
        for archivo in glob.glob(os.getcwd()+f'/{var}_*.csv'):
            try:
                data = pandas.read_csv(archivo, sep=';')
            except:
                print('No hay datos disponibles para la peticion requerida')
                os.remove(archivo)
            total_data = pandas.concat([total_data, data])
            os.remove(archivo)
            
        total_data[total_data.columns[pos]] = total_data.iloc[:,pos].replace(",",".", regex= True).astype(float)
        
        return round(total_data[total_data.columns[pos]].sum(), 2)
