# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 14:08:04 2023

@author: german.carneros.ext
"""
from datetime import datetime
import json
import glob
from datetime import timedelta
from .SAIH.saihinformation import SAIHInformation
from .AEMET.aemet import Aemet
from apps.transactions.api.processes.errores.class_Errores import Errores
import os
import sys
import pandas as pd
project_dir = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(project_dir)


def get_data_meteo(city: str, days: int, end_date, preds=False):
    '''
    This function returns one DataFrame with the meteo data for each city

    Parameters
    ----------
    city : str
        Name of the city to get the data.
    days : int
        Number of previous days to get the data.
    end_date : 
        Last day of the meteo data we want to get.

    Returns
    -------
    prec_temp_Roquetas : DataFrame
    prec_temp_Granada : DataFrame
    prec_temp_Marbella : DataFrame

    '''
    star_date = end_date - timedelta(days=days - 1)

    if city == 'Roquetas de Mar':
        if preds==False:
            aemet = Aemet(idema=['fecha', 'tmed', 'prec'], mun_code='6293X')
            ok, prec_temp = aemet.get_climatological_info(
                str(star_date), str(end_date))
        else:
            aemet = Aemet(idema=['fecha', 'tmed', 'prec','tmax'], mun_code='6325O')
            ok, prec_temp = aemet.get_climatological_info(
                str(star_date)[:10], str(end_date)[:10])

        data_meteo = pd.json_normalize(prec_temp).set_index('fecha')
        data_meteo.index = pd.to_datetime(data_meteo.index, format='%Y-%m-%d')

    elif city == 'Granada' or city == 'Armilla':
        if preds==False:
            aemet = Aemet(idema=['fecha', 'tmed', 'prec'], mun_code='5514')
            ok, prec_temp = aemet.get_climatological_info(
                str(star_date), str(end_date))
        else:
            aemet = Aemet(idema=['fecha', 'tmed', 'prec','tmax'], mun_code='5514')
            ok, prec_temp = aemet.get_climatological_info(
                str(star_date)[:10], str(end_date)[:10])             

        data_meteo = pd.json_normalize(prec_temp).set_index('fecha')
        data_meteo.index = pd.to_datetime(data_meteo.index, format='%Y-%m-%d')
    elif city == 'Marbella':
        if preds==False:
            si = SAIHInformation()
            prec_Marbella = si.get_data_period(2, '016P01', 1, star_date.strftime(
                "%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))['Acumulado (l/m2)']
            temperature_Marbella = si.get_data_period(2, '016M02', 60, star_date.strftime(
                "%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))  # No hay datos diarios en SAIH para temperatura en esta estacion
            temperature_Marbella = temperature_Marbella['Temperatura (ºC)'].resample(
                'D').mean()

            data_meteo = pd.concat([temperature_Marbella, prec_Marbella], axis=1).rename(
                columns={'Temperatura (ºC)': 'tmed', 'Acumulado (l/m2)': 'prec'})
            data_meteo.index = pd.to_datetime(data_meteo.index, format='%Y-%m-%d')
        else:
            si = SAIHInformation()
            prec_Marbella = si.get_data_period(2, '016P01', 1, star_date.strftime(
                "%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))['Acumulado (l/m2)']
            temperature_Marbella = si.get_data_period(2, '016M02', 60, star_date.strftime(
                "%d/%m/%Y"), end_date.strftime("%d/%m/%Y")) 
            temperature_Marbella = temperature_Marbella['Temperatura (ºC)'].resample(
                'D').max()

            data_meteo = pd.concat([temperature_Marbella, prec_Marbella], axis=1).rename(
                columns={'Temperatura (ºC)': 'tmax', 'Acumulado (l/m2)': 'prec'})
            data_meteo.index = pd.to_datetime(data_meteo.index, format='%Y-%m-%d')            
    else:
        data_meteo = pd.DataFrame()

    return data_meteo


def get_data_sector(file_sector_info: str, days_limit: int = 60):
    '''
    This function return the data in the required format from the input excel

    Parameters
    ----------
    days_limit : int
        Number of previous days to cut the input data in order to optimize the execution time, remaining its statistic sense. The default is 60.

    Returns
    -------
    df : DataFrame

    '''

    # file_name = glob.glob('rest_api_cetaqua/files/sector_info.xlsx')
    file_name = glob.glob('rest_api_cetaqua/files/' + file_sector_info)

    error = Errores.file_format(
        Errores, file_name=file_name[0], extension='.xlsx')
    if error != True:
        return error

    df = pd.read_excel(file_name[0])
    error = Errores.check_columns(Errores, df=df, column_list=[
                                  'Fecha', 'Caudal suministrado', 'Volumen suministrado diario', 'Average pressure'])
    if error != True:
        return error

    df.rename(columns={'Caudal suministrado': 'Caudal',
              'Volumen suministrado diario': 'Volumen', 'Average pressure': 'Presion'}, inplace=True)
    tipos_columnas = {
        'Fecha': datetime,
        'Caudal': float,
        'Volumen': float,
        'Presion': float
    }
    Errores.check_columns_type(Errores, df=df, columns_types=tipos_columnas)
    df.set_index('Fecha', inplace=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S')
    df.sort_index(inplace=True)
    df.dropna(how='all', inplace=True)
    if df.index[-1].hour != 23:
        df = df[df.index < df.index[-1] - timedelta(hours=df.index[-1].hour)]

    df = df[df.index > df.index[-1] - timedelta(days=days_limit)]
    df = df.resample('H').mean()

    df.drop(df.index[-1], inplace=True)

    return df


def get_data_param(data_name: str, days_limit: int = 60):
    '''
    This function return the parameter data to calculate the leak risk.

    Parameters
    ----------
    data_name : str
        Name of the file where the parameters data is saved.

    '''
    # Errores.file_format(data_name, '.json')
    # with open(f'{data_name}', 'r') as file:
    # param = json.load(file)
    param = data_name
    error = Errores.check_fields_json(Errores, param, [
                                      'flow', 'minFlow', 'dailyVolume', 'pressure', 'minFlowMultmeanFlow', 'minFlowDivmeanFlow', 'meteo'])
    if error != True:
        return error

    error = Errores.check_fields_json(
        Errores, param['flow'], ['active', 'meanWeekDays', 'hours', 'tolerance'])
    if error != True:
        return error

    error = Errores.check_fields_json(Errores, param['minFlow'], [
                                      'active', 'movingAverageDays', 'fixedAverageDays', 'weightAverage', 'weightDeviation', 'tolerance'])
    if error != True:
        return error

    error = Errores.check_fields_json(Errores, param['dailyVolume'], [
                                      'active', 'movingAverageDays', 'fixedAverageDays', 'weightAverage', 'weightDeviation', 'tolerance'])
    if error != True:
        return error

    error = Errores.check_fields_json(Errores, param['pressure'], [
                                      'active', 'movingAverageDays', 'weightAverage', 'weightDeviation'])
    if error != True:
        return error

    error = Errores.check_fields_json(Errores, param['minFlowMultmeanFlow'], [
                                      'active', 'movingAverageDays', 'weightAverage', 'weightDeviation'])
    if error != True:
        return error

    error = Errores.check_fields_json(Errores, param['minFlowDivmeanFlow'], [
                                      'active', 'movingAverageDays', 'weightAverage', 'weightDeviation'])
    if error != True:
        return error

    error = Errores.check_fields_json(Errores, param['meteo'], ['active'])
    if error != True:
        return error

    tipos_campos = {
        'active': bool,
        'meanWeekDays': int,
        'hours': int,
        'tolerance': float,
        'movingAverageDays': int,
        'fixedAverageDays': int,
        'weightAverage': float,
        'weightDeviation': float
    }
    Errores.check_fields_type(Errores, param['flow'], tipos_campos)
    Errores.check_fields_type(Errores, param['minFlow'], tipos_campos)
    Errores.check_fields_type(Errores, param['dailyVolume'], tipos_campos)
    Errores.check_fields_type(Errores, param['pressure'], tipos_campos)
    Errores.check_fields_type(
        Errores, param['minFlowMultmeanFlow'], tipos_campos)
    Errores.check_fields_type(
        Errores, param['minFlowDivmeanFlow'], tipos_campos)
    Errores.check_fields_type(Errores, param['meteo'], tipos_campos)
    return param
