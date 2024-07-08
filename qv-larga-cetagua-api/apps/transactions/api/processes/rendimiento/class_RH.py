# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 12:40:57 2023

@author: german.carneros.ext
"""
import os
import glob
import json
import random
import joblib
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import pacf

from apps.transactions.api.processes.errores.class_Errores import Errores
from apps.transactions.api.processes.fugas.get_data_Lagar import get_data_meteo
from rest_framework.response import Response
from rest_framework import status

class RH:
    
    def __init__(self, city:str, sector_salida:str, year_output:int, bimestre_salida:int):
        self.city = city
        
        with open(f'rest_api_cetaqua/files/performance_hydraulic/data/{self.city}/{self.city}.json', 'r') as archivo:
            data_file = json.load(archivo)
        self.errors=[]
        self.output_sector = data_file[sector_salida]
        self.output_year = year_output
        self.output_period = bimestre_salida
        self.get_data()
        
    def get_data(self):
        wd =  os.getcwd()
        path_registrados = glob.glob(wd + f'/rest_api_cetaqua/files/performance_hydraulic/data/{self.city}/registrado/*')
        
        datos_registrados = pd.DataFrame()
        tipos_columnas = {
            'Registrado' : float,
            'Contrato' : int,
            'Ajustes_Reparto' : float,
            'Ajustes_Estimado' : float,
            'Otros_Ajustes' : float,
            'Pocperiodi' : int,
            'M3 Estimados' : float,
            'M3 Consumidos' : float,
            'Lectura Actual Esf.1' : float,
            'Lectura Anterior Esf.1' : float,
            'Periodicidad' : str
            }

        for file in path_registrados:
            error_xlsx = Errores.file_format(Errores, file,'.xlsx')
            error_csv = Errores.file_format(Errores, file,'.csv')
            if error_xlsx != True and error_csv != True:
                self.errors.append(error_xlsx)
                return None
            
            datos = pd.read_excel(file)
            datos_registrados = pd.concat([datos_registrados, datos])
        if self.city=='Roquetas de Mar':
            try:
                path_telelectura = glob.glob(wd + f'/rest_api_cetaqua/files/performance_hydraulic/data/{self.city}/telelectura/Telelectura*.xlsx')
                datos_contadores_telectura = pd.read_csv(path_telelectura[0])
                
                error = Errores.check_columns(Errores, datos_contadores_telectura, ['Contrato'])
                if error != True:
                    self.errors.append(error)
                    return None
                Errores.check_columns_type(Errores,datos_contadores_telectura, tipos_columnas)
                cont_telelectura = list(set(datos_contadores_telectura['Contrato']))
            except:
                cont_telelectura = []

            error = Errores.check_columns(Errores, datos_registrados, ['Sector', 'Registrado', 'Contrato', 'Ajustes_Reparto', 'Ajustes_Estimado', 'Otros_Ajustes', 'Periodo', 'Pocperiodi'])            
            if error != True:
                self.errors.append(error)
                return None
            datos_registrados = datos_registrados[datos_registrados['Sector'] == self.output_sector]
            Errores.check_columns_type(Errores, datos_registrados, tipos_columnas)
            datos_registrados['Litros_Registrados'] = pd.to_numeric(datos_registrados['Registrado'])
            datos_registrados['Contrato'] = pd.to_numeric(datos_registrados['Contrato'])
            datos_registrados.dropna(subset='Contrato', inplace=True)
            datos_registrados['Litros_Ajuste'] = pd.to_numeric(datos_registrados['Ajustes_Reparto'] + datos_registrados['Ajustes_Estimado'] + datos_registrados['Otros_Ajustes'])
            datos_registrados['Litros_Facturados'] = pd.to_numeric(datos_registrados['Litros_Registrados'] + datos_registrados['Litros_Ajuste'])
            datos_registrados['Año'] = datos_registrados['Periodo'].apply(lambda x: int(str(x)[:4]))
            datos_registrados['Bimestre'] = datos_registrados.apply(lambda row: int(int(str(row['Periodo'])[-2:]) // 2) + int(str(row['Periodo'])[-2:]) % 2 if row['Pocperiodi'] == 1 else int(str(row['Periodo'])[-2:]), axis=1)
            try:
                datos_registrados['Tipo_Lectura'] = datos_registrados['Contrato'].apply(lambda x: 'T' if x in cont_telelectura else 'M')
            except:
                datos_registrados['Tipo_Lectura'] =  'M'        
            datos_registrados = datos_registrados[datos_registrados['Año'] == self.output_year]
            datos_registrados = datos_registrados[datos_registrados['Bimestre'] == self.output_period]
            
        elif self.city=='Marbella':
            cont_telelectura = []

            error = Errores.check_columns(Errores, datos_registrados, ['Sector', 'Registrado', 'Contrato', 'Ajustes_Reparto', 'Ajustes_Estimado', 'Otros_Ajustes', 'Periodo', 'Pocperiodi'])            
            if error != True:
                self.errors.append(error)
                return None
            datos_registrados = datos_registrados[datos_registrados['Sector'] == self.output_sector]
            Errores.check_columns_type(Errores, datos_registrados, tipos_columnas)
            try:
                datos_registrados['Litros_Registrados'] = pd.to_numeric(datos_registrados['Registrado'])
                datos_registrados['Contrato'] = pd.to_numeric(datos_registrados['Contrato'])
                datos_registrados.dropna(subset='Contrato', inplace=True)
                datos_registrados['Litros_Ajuste'] = pd.to_numeric(datos_registrados['Ajustes_Reparto'] + datos_registrados['Ajustes_Estimado'] + datos_registrados['Otros_Ajustes'])
                datos_registrados['Litros_Facturados'] = pd.to_numeric(datos_registrados['Litros_Registrados'] + datos_registrados['Litros_Ajuste'])
                datos_registrados['Año'] = datos_registrados['Periodo'].apply(lambda x: int(str(x)[:4]))
                datos_registrados['Bimestre'] = datos_registrados.apply(lambda row: int(int(str(row['Periodo'])[-2:]) // 2) + int(str(row['Periodo'])[-2:]) % 2 if row['Pocperiodi'] == 1 else int(str(row['Periodo'])[-2:]), axis=1)
                try:
                    datos_registrados['Tipo_Lectura'] = datos_registrados['Contrato'].apply(lambda x: 'T' if x in cont_telelectura else 'M')
                except:
                    datos_registrados['Tipo_Lectura'] =  'M'            
                datos_registrados = datos_registrados[datos_registrados['Año'] == self.output_year]
                datos_registrados = datos_registrados[datos_registrados['Bimestre'] == self.output_period]
            except:
                response = {'Los ficheros de entrada no contienen los datos necesarios'}
                return Response({"Error":response}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                
            
        elif self.city == 'Armilla':
            cont_telelectura = []
            
            error = Errores.check_columns(Errores, datos_registrados, ['Sector', 'Año', 'Contrato', 'M3 Estimados', 'M3 Consumidos', 'Lectura Actual Esf.1', 'Lectura Anterior Esf.1', 'Periodo', 'Periodicidad'])            
            if error != True:
                self.errors.append(error)
                return None
            
            datos_registrados = datos_registrados[datos_registrados['Sector'] == self.output_sector]
            datos_registrados = datos_registrados[datos_registrados['Año'] == self.output_year]
            Errores.check_columns_type(Errores, datos_registrados, tipos_columnas)
            datos_registrados['Fecha_Lectura'] = datos_registrados['Fecha Lectura Actual']
            datos_registrados.dropna(subset='Contrato', inplace=True)
            datos_registrados.rename(columns={'M3 Estimados':'Litros_Ajuste', 'M3 Consumidos':'Litros_Facturados'}, inplace=True)
            datos_registrados['Litros_Registrados'] = pd.to_numeric(datos_registrados['Lectura Actual Esf.1'] - datos_registrados['Lectura Anterior Esf.1'])
            try:
                datos_registrados['Tipo_Lectura'] = datos_registrados['Sistema Lectura'].apply(lambda x: 'T' if x == 'Leer por telelectura' else 'M')
            except:
                datos_registrados['Tipo_Lectura'] =  'M'
            datos_registrados['Bimestre'] = datos_registrados.apply(lambda x: x['Periodo'] if x['Periodicidad'] == 'BIMESTRAL' else (int(x['Periodo']) // 2 + int(x['Periodo']) % 2), axis=1)

            datos_registrados = datos_registrados[datos_registrados['Bimestre'] == self.output_period]

        elif self.city == 'Granada':
            try:
                datos_contadores_telectura = pd.read_csv(wd + f'/rest_api_cetaqua/files/performance_hydraulic/data/{self.city}/Contadores con TL.csv')
                cont_telelectura = list(set(datos_contadores_telectura['Contrato']))
            except:
                cont_telelectura = []

            datos_registrados['Fecha_Lectura'] = datos_registrados['Fecha Lectura Actual']
            datos_registrados.dropna(subset='Contrato', inplace=True)
            datos_registrados.rename(columns={'M3 Estimados':'Litros_Ajuste', 'M3 Consumidos':'Litros_Facturados'}, inplace=True)
            datos_registrados['Litros_Registrados'] = pd.to_numeric(datos_registrados['Lectura Actual Esf.1'] - datos_registrados['Lectura Anterior Esf.1'])
            try:
                datos_registrados['Tipo_Lectura'] = datos_registrados['Contrato'].apply(lambda x: 'T' if x in cont_telelectura else 'M')
            except:
                datos_registrados['Tipo_Lectura'] =  'M'            
            datos_registrados['Bimestre'] = datos_registrados.apply(lambda x: x['Periodo'] if x['Periodicidad'] == 'BIMESTRAL' else (int(x['Periodo']) // 2 + int(x['Periodo']) % 2), axis=1)


        datos_registrados['Litros_Telelectura'] = np.zeros(len(datos_registrados))
        datos_registrados = datos_registrados[datos_registrados['Litros_Registrados'] >= 0]
        datos_registrados = datos_registrados[['Sector', 'Contrato', 'Año', 'Bimestre', 'Litros_Registrados', 'Litros_Ajuste', 'Litros_Facturados', 'Litros_Telelectura', 'Tipo_Lectura','Fecha_Lectura']]
        datos_registrados['Contrato'] = datos_registrados['Contrato'].apply(int)

        self.data = datos_registrados

    def create_historicals (self):
        check = self.df.index<self.starting_date
        aux = self.df[['v1']][check].groupby(by=[self.df[['v1']][check].index.month])
     
        self.hist_q2 = aux.mean()
         
        self.df_input = self.df.dropna().copy()
        self.df_input2 = self.df_input[self.df_input.index<self.starting_date]
        
        self.predict_Qn()
            
        
    def predict_Qn (self):
        self.df_prec_historicos_q2 = self.df_input2[['v1']].copy()

        for i in range(1,13):
            new_moth = self.df_input2.index[-1] + relativedelta(months=i)

            self.df_prec_historicos_q2 = pd.concat([self.df_prec_historicos_q2, pd.DataFrame([self.hist_q2.v1[new_moth.month]], columns=self.df_prec_historicos_q2.columns)], ignore_index=True)
        
        dates = pd.date_range(self.df_input2.index[0], periods=len(self.df_input2)+12, freq='MS')   
        self.df_prec_historicos_q2.set_index(dates, inplace=True)     
        

    def scenario_series(self):
        self.df_q2 = pd.DataFrame()
        self.df_q2.insert(0,'v1', self.df_prec_historicos_q2.shift(self.shift_vble_1).rolling(self.rolling_vble_1).sum())
        self.df_q2.insert(0,'y', self.df.y)
            
            
    def scenario_series_pred(self):
        # Predicción series scenarios
        scenarios = [self.df_q2]
        scenarios_names = ['pred']

        self.result_table = pd.DataFrame()
        for scenario, scenario_name in zip(scenarios, scenarios_names):
            #print(f'---> \n {scenario}')
            df_forecast =scenario.copy()
            forecast_start = self.starting_date
            
            df_ms = df_forecast[df_forecast.index < forecast_start].dropna() ###
            val_ms = df_forecast[df_forecast.index >= forecast_start]

            df_ms_scaled = self.scaler.fit_transform(np.array(df_ms))
            val_ms_scaled = self.scaler.transform(np.array(val_ms))
            df_tr = pd.DataFrame(df_ms_scaled, index=df_ms.index, columns=list(df_forecast.columns))
            df_val = pd.DataFrame(val_ms_scaled, index=val_ms.index, columns=list(df_forecast.columns))
            df_full = pd.concat([df_tr, df_val])

            df_ms = df_tr.copy()
            val_ms = df_val.copy()
            df_forecast = df_full.copy()

            data_ap = df_ms.copy()
            
            n_lags_max = min(12,int((len(data_ap)/2)-1))
            lags, data_ap_2 = self.__create_lag_features(data_ap, n_lags_max, self.threshold)
            lags.remove(0)
            
            data_ap = self.__lagger(data_ap, lags)
            y = data_ap.dropna().y
            X = data_ap.dropna().drop(['y'], axis=1)

            self.model.fit(X, y)
            
            result_q = self.__quartile_rec_forecast(self.model, df_forecast, df_ms, val_ms, lags, self.n_pred)
            
            self.result_table.insert(scenarios.index(self.df_q2),scenario_name,result_q)
            
            
    def __quartile_rec_forecast(self, model, df, df_ms, val_ms, nlags, n_steps):
        rec_fcast = self.__forecast_multi_recursive(df, df_ms, model, nlags, n_steps)
        
        val=val_ms.drop(['y'], axis=1)
        val.insert(0,'y',rec_fcast)
        val.dropna(inplace=True)
        rec_fcast_inverse = self.scaler.inverse_transform(val)
        rec_fcast_inverse = rec_fcast_inverse[:,0]
        rec_fcast=pd.DataFrame(rec_fcast_inverse, index=rec_fcast.index, columns= ['y'])
        
        return rec_fcast
    

    def __forecast_multi_recursive(self,data_full, data, model, lags=10, n_steps=4, step="MS"):
        
        # get the dates to forecast
        last_date = data.index[-1] + relativedelta(months=1)
        fcast_range = pd.date_range(last_date, periods=n_steps, freq=step)
        
        fcasted_values = []
        target = pd.DataFrame()
        target.insert(0,'y',data.y)
        features_todo = data_full.drop(['y'], axis=1)
        
        for date in fcast_range:
            new_point = fcasted_values[-1] if len(fcasted_values) > 0 else 0.0
            df2 = pd.DataFrame([new_point], index = [date], columns = list('y'))
            target = pd.concat([target, df2])
            
            # Adding the lag of the target variable
            features = features_todo.copy()
            for i in lags:
                features["lag_{}".format(i)] = target.y.shift(i)

            x = pd.DataFrame()
            x = features.dropna()

            predictions = model.predict(x)  
            fcasted_values.append(predictions[-1])
            target.iloc[-1] = predictions[-1]
            
        
        return pd.Series(index=fcast_range, data=fcasted_values)


    def __lagger(self,data, nlags):
        for i in nlags:
            data["lag_{}".format(i)] = data.y.shift(i)
            
        return data
        
    
    def __create_lag_features(self,target, lags_max=12, thres=0.10):
        target = target.iloc[:,0]

        partial = pd.Series(data=pacf(target, nlags=lags_max))
        lags = list(partial[np.abs(partial) >= thres].index)
        
        df = pd.DataFrame()
        for l in lags:
            df[f"lag_{l}"] = target.shift(l)
            
        features = df
        features.index = target.index
        
        return lags, features
    
    def pred_suministrado(self,data):
        self.n_pred = 1
        
        try:
            self.df = data.copy()
            tmax = get_data_meteo(self.city,1800,pd.to_datetime(str(data.index[-1]+ relativedelta(months=1))[:10]),True)[['tmax']]
            self.df.insert(1,'v1',tmax.tmax)
            self.df.columns = ['y','v1']
           
            self.configuration = pd.read_csv(f'apps/transactions/api/processes/rendimiento/modelos/{self.output_sector}_estructura.csv', sep=';')
            self.shift_vble_1 = self.configuration.shift_vble_1[0]
            self.rolling_vble_1 = self.configuration.rolling_vble_1[0]
            self.threshold = self.configuration.thres[0]
            self.model = joblib.load(f'apps/transactions/api/processes/rendimiento/modelos/{self.output_sector}_modelo.pkl')
           
            self.starting_date = self.df.index[-1] + relativedelta(months=1)
            
            self.scaler = StandardScaler()
            
            self.create_historicals()
            self.scenario_series()
            self.scenario_series_pred()
        
        except:
            val_pred = data[data.index.month==data.index[-1].month+1].mean()
            self.result_table = pd.DataFrame(columns=['pred'],data=[val_pred[0]])
            

        return self.result_table   
    
    
    def bimonthly(self,data):
        data.dropna(inplace=True)
        ini = data[data.index.month % 2 == 1].index[0]
        data = data[data.index>=ini]
        
        data = data.rolling(2).sum()
        data = data[data.index.month % 2 == 0]
        
        return data

    def estimacion_registrado(self,suministrado, registrado, pred_suministrado): 
        vol_min = suministrado.resample('D').min()*24
        vol_min = vol_min.resample('MS').sum() 
        
        suministrado = suministrado.resample('H').mean() 
        suministrado = suministrado.resample('MS').sum()
        suministrado_bi = self.bimonthly(suministrado)
        registrado_bi = self.bimonthly(registrado)
        df_bi = pd.concat([suministrado_bi,registrado_bi],axis=1).dropna()
        df_bi.columns = ['suministrado','registrado']
        
        k = df_bi.registrado/df_bi.suministrado
        coef = 1 - k 
        vol_perdida = vol_min.iloc[-1,0] * coef.median()
        
        if pred_suministrado.index[-1] > suministrado.index[-1]:
            reg_est = pred_suministrado.iloc[-1,0] - vol_perdida   
        else:
            reg_est = suministrado.iloc[-1,0] - vol_perdida
        
        return reg_est

    def RH_algorithm(self, file_suplied_name):
        
        self.rh = pd.DataFrame()
        
        tipos_columnas = {'Caudal suministrado' : float}
        sec = self.output_sector
        df_sector = self.data[self.data['Sector'] == sec]
        df_sector.reset_index(drop=True, inplace=True)
        
        try:
            df_suministrado = pd.read_excel(f'rest_api_cetaqua/files/{file_suplied_name}')
            print('df_suministrado', df_suministrado)
            error= Errores.check_columns(Errores, df_suministrado, ['Caudal suministrado'])

            if error != True:
                self.errors.append(error)
                return None
            Errores.check_columns_type(Errores, df_suministrado, tipos_columnas)
            df_suministrado.set_index(df_suministrado.columns[0], inplace=True)
            df_suministrado.index = pd.to_datetime(df_suministrado.index, format='%Y-%m-%d %H:%M:%S')
            suministrado_base = df_suministrado.copy()
            df_suministrado = df_suministrado.resample('H').mean()
            df_suministrado = df_suministrado.resample('MS').sum()
            suministrado = True
        except:
            suministrado = False
        
        for i in range(len(df_sector)):
            if (pd.isna(df_sector.iloc[i]['Litros_Registrados'])):
                df_sector.loc[i,'Litros_Registrados'] = 0
            if (pd.isna(df_sector.iloc[i]['Litros_Ajuste'])):
                df_sector.loc[i,'Litros_Ajuste'] = 0
            if (pd.isna(df_sector.iloc[i]['Litros_Facturados'])):
                df_sector.loc[i,'Litros_Facturados'] = df_sector.iloc[i]['Litros_Registrados'] - df_sector.iloc[i]['Litros_Ajuste']
                
            if df_sector.iloc[i]['Tipo_Lectura'] == 'T':
                df_sector.loc[i, 'Litros_Telelectura'] = df_sector.iloc[i]['Litros_Registrados']
                df_sector.loc[i, 'Litros_Registrados'] = 0
                
        df_año = df_sector[df_sector['Año'] == self.output_year]
        df_bimestre = df_año[df_año['Bimestre'] == self.output_period]
        num_contratos = len(set(df_bimestre['Contrato']))
        df_bimestre = df_bimestre.drop(columns=['Contrato','Tipo_Lectura'])
        df_bimestre = df_bimestre.groupby('Bimestre').agg({'Sector': 'first', 'Año': 'first', 'Litros_Registrados': 'sum', 'Litros_Ajuste': 'sum', 'Litros_Telelectura': 'sum', 'Litros_Facturados': 'sum'})

        df_bimestre['Num_contratos'] = num_contratos
        df_bimestre['Sector'] = sec
        if suministrado:
            df_bimestre['Litros_Suministrados'] = df_suministrado['Caudal suministrado'][(df_suministrado.index.year == self.output_year) & ((df_suministrado.index.month == self.output_period*2) | (df_suministrado.index.month == self.output_period*2 - 1))].sum()
        else:
            df_bimestre['Litros_Suministrados'] = np.nan
        self.rh = pd.concat([self.rh, df_bimestre])
        self.rh.reset_index(inplace=True)
        self.rh['Porcentaje_Registrado'] = round((self.rh['Litros_Registrados'] / self.rh['Litros_Facturados']) * 100, 2)
        self.rh['Porcentaje_Ajuste'] = round((abs(self.rh['Litros_Ajuste']) / self.rh['Litros_Facturados']) * 100, 2)
        self.rh['Porcentaje_Telelectura'] = round((self.rh['Litros_Telelectura'] / self.rh['Litros_Facturados']) * 100, 2)
        self.rh['Porcentaje_RH_total'] = round((self.rh['Litros_Facturados'] / self.rh['Litros_Suministrados']) * 100, 2)
        # self.rh['Suministrado_esperado'] = round(random.choices(range(int(self.rh['Litros_Registrados'][0]*0.9),int(self.rh['Litros_Registrados'][0]*1.1)),k=1)[0], 2)
        try:
            df_pred_suministrado = self.pred_suministrado(df_suministrado)
            self.rh['Suministrado_esperado'] = round(df_pred_suministrado.pred[0], 2)            
        except:
            self.rh['Suministrado_esperado'] = np.nan
        # self.rh['Registrado_esperado'] = round(random.choices(range(int(self.rh['Litros_Registrados'][0]*0.6),int(self.rh['Litros_Registrados'][0]*0.7)),k=1)[0], 2)    
        try:
            df_registrado = self.data[['Fecha_Lectura','Litros_Registrados']] 
            df_registrado.set_index('Fecha_Lectura',inplace=True)
            df_registrado = df_registrado.resample('MS').sum()
            self.rh['Registrado_esperado'] = round(self.estimacion_registrado(suministrado_base, df_registrado, df_pred_suministrado), 2)            
        except:
            if self.rh['Suministrado_esperado'].isnull():
                self.rh['Registrado_esperado'] = round(random.choices(range(int(self.rh['Litros_Registrados'][0]*0.85),int(self.rh['Litros_Registrados'][0]*0.95)),k=1)[0], 2)
            else:
                self.rh['Registrado_esperado'] = round(self.rh['Suministrado_esperado']*0.8,2)

        self.rh['RH_esperado'] = round((self.rh['Registrado_esperado'] / (self.rh['Suministrado_esperado'])) * 100, 2)
        self.rh['RH_esperado'] = min(100,self.rh['RH_esperado'][0])
        self.rh = self.rh[['Sector', 'Año', 'Bimestre', 'Num_contratos', 'Litros_Registrados', 'Litros_Ajuste', 'Litros_Telelectura', 'Litros_Facturados', 'Litros_Suministrados', 'Porcentaje_Registrado', 'Porcentaje_Ajuste', 'Porcentaje_Telelectura', 'Porcentaje_RH_total', 'Suministrado_esperado', 'Registrado_esperado', 'RH_esperado']]
        self.rh = round(self.rh,2)

        try:
            return self.rh.to_dict(orient='records')[0]
        except:
            error = {'No hay datos disponibles para esta combinacion de inputs.'}
            response = Response({"Error":error}, status=status.HTTP_400_BAD_REQUEST)
            self.errors.append(response)
            return None