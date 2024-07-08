# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:59:18 2023

@author: german.carneros.ext
"""
import numpy as np
from datetime import timedelta


def mean_ds(pos_ini, num_weeks, data):
    '''
    Funcion para calcular la media por dias de la semana, con el mismo dia de semanas anteriores

    '''
    aux = 0
    for i in range(1, num_weeks+1):
        aux += data[pos_ini-timedelta(weeks=i)]
    return aux/num_weeks


def prod(data, k):
    '''
    Funcion para obtener los limites superior e inferior de la envolvente

    '''
    aux = [i*k for i in data]
    return aux


def ind_envolvente(serie, days, weeks_mean, umbral_h, tolerancia):
    '''
    Funcion que calcula el indicador de envolvente, lo grafica y devuelve los dias que han sido marcados como anomalos por este indicador

    '''
    serie.dropna(inplace=True)
    data = serie[serie.index >= str(serie.index[-days*24].replace(hour=0))]
    datetime = data.index

    cont_env = np.zeros(days)
    # variable para comprobar el numero de horas que se ha salido de la envolvente
    cont_envolvente = 0
    dia_ant = -1

    # Ventanas para calcular la envolvente
    mean_envolvente = []
    data_mean = serie[(serie.index < str(serie.index[-1].replace(hour=0))) & (
        serie.index >= str(serie.index[-(days + weeks_mean*7)*24].replace(hour=0)))]
    for i in data.index:
        mean_envolvente.append(mean_ds(i, weeks_mean, data_mean))

    # Check si el caudal horario se sale de la envolvente calculada como la media con los valores de los mismos dias de semanas anteriores
    for i in range(len(data)):
        if data[i] > mean_envolvente[i]*(1+tolerancia) or data[i] < mean_envolvente[i]*(1-tolerancia):
            cont_envolvente += 1
        else:
            cont_envolvente = 0

        if cont_envolvente >= umbral_h:
            # Una vez que supere un numero determinado de horas consecutivas fuera de la envolvente pintamos ese dia como anomalo
            dia = int(i/24)

            cont_envolvente = 0

            if dia != dia_ant:
                dia_ant = dia
                # marcamos ese dia como anomalo para comprobar luego los indicadores que saltan simultaneamente
                cont_env[dia] = 1

    cont_env_exp = [int(elemento) for elemento in cont_env for _ in range(24)]

    return data.tolist(), datetime.tolist(), cont_env_exp, mean_envolvente


def ind_medias(serie, days, ventana_movil, peso_media, peso_std, media_fija=False, ventana_fija=0, tolerancia=0):
    '''
    Funcion que calcula el indicador de las medias, tanto fija como móvil, lo grafica y devuelve los dias que han sido marcados como anomalos por este indicador

    '''
    cont_env = np.zeros(days)
    pos = 0
    if ((days + max(ventana_movil, ventana_fija))+2) > len(serie):
        ventana_fija = len(serie) - 3 - days
    data_pre = serie[(serie.index < str(serie.index[-1])) & (serie.index >=
                                                             str(serie.index[-(days + max(ventana_movil, ventana_fija))-2]))]

    data = serie[serie.index >= str(serie.index[-days])]

    datetime = data.index

    for day in data.index[:-1]:
        med_movil = peso_media * \
            data_pre[(data_pre.index >= day - timedelta(days=ventana_movil))
                     & (data_pre.index < day)].mean()
        std_movil = peso_std * \
            data_pre[(data_pre.index >= day - timedelta(days=ventana_movil))
                     & (data_pre.index < day)].std()

        if media_fija:
            med_fija = data_pre[(
                data_pre.index >= day - timedelta(days=ventana_fija)) & (data_pre.index < day)].mean()

        # Comprobamos si supera el indicador de media y desv tipica
        if (data[day] > med_movil + std_movil) or (data[day] < med_movil - std_movil):
            cont_env[pos] = 1
            data_pre.drop(day, inplace=True)

        # Comprobamos si supera el indicador de media fija
        elif media_fija and ((data[day] > (1+tolerancia)*med_fija) or (data[day] < (1-tolerancia)*med_fija)):
            cont_env[pos] = 1
            data_pre.drop(day, inplace=True)

        else:   # Si el dia no es anomalo, borramos el primer dia de las ventanas moviles para hacer los calculos a partir del dia siguiente
            data_pre.drop(data_pre.index[0], inplace=True)
        pos = pos + 1

    cont_env = [int(elemento) for elemento in cont_env]

    return data.tolist(), datetime.tolist(), cont_env


def ind_umbral(serie, days, tolerancia):
    '''
    Funcion que calcula el indicador de umbral para la telelectura, lo grafica y devuelve los dias que han sido marcados como anomalos por este indicador

    '''
    cont_env = np.zeros(days)
    data = serie[serie.index >= str(serie.index[-days-1])]
    datetime = data.index

    for i in range(len(data)-1):
        if data[i] >= 1 + tolerancia:
            cont_env[i] = 1

    cont_env = [int(elemento) for elemento in cont_env]

    return data.tolist(), datetime.tolist(), cont_env
