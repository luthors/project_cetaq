import os
from datetime import datetime
import pandas as pd
import numpy as np
from rest_framework.response import Response
from rest_framework import status


class Errores:
    """_summary_
    """
    def file_format(self, file_name:str, extension:str='.xlsx'):
        if os.path.splitext(file_name)[1] != extension:
            response=f"415 --> El archivo {file_name.split('/')[-1] if len(file_name.split('/')) > 1 else file_name} no tiene la extension requerida: {extension}"
            return Response({"Error":response}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        else:
            return True
    def check_columns(self, df, column_list):
        if set(column_list).issubset(df.columns):
            return True
        else: 
            response=f"400 --> Faltan las columnas: {list(set(column_list) - set(df.columns))}"
            return Response({"Error":response}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)    
        # barckR --> petición ---- code_cetaqua: 400 es la loǵica
    def check_fields_json(self, json, field_list):
        if not set(field_list) - set(json.keys()):
            return True
        else:
            response=f"400 --> Faltan los campos: {list(set(field_list) - set(json.keys()))}"
            return Response({"Error":response, "code_cetaqua":400}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def check_columns_type(self, df, columns_types):
        """
        Elimina las filas del DataFrame cuyos elementos en cada columna no sean del tipo especificado en tipos_columnas.
        
        Parámetros:
        - dataframe: DataFrame que se va a limpiar.
        - tipos_columnas: Diccionario que especifica el tipo esperado para cada columna. Las claves deben ser los nombres de las columnas.
        """
        for columna, tipo_esperado in columns_types.items():
            if columna in df.columns:
                for i in df.index:
                    try:
                        if df.loc[i,columna] != np.nan:
                            if tipo_esperado == datetime:
                                    df.loc[i,columna] = pd.to_datetime(df.loc[i][columna])
                            else:
                                df.loc[i,columna] = tipo_esperado(df.loc[i][columna])
                    except:
                        df.loc[i,columna] = np.nan
        return df
    def check_fields_type(self, json_data, fields_types):
        """
        Elimina las filas del JSON cuyos elementos en cada campo no sean del tipo especificado en fields_types.
        
        Parámetros:
        - json_data: Diccionario que representa el JSON.
        - fields_types: Diccionario que especifica el tipo esperado para cada campo. Las claves deben ser los nombres de los campos.
        """
        for campo, tipo_esperado in fields_types.items():
            if campo in json_data:
                try:
                    if tipo_esperado == datetime:
                        json_data[campo] = pd.to_datetime(json_data[campo])
                    else:
                        json_data[campo] = tipo_esperado(json_data[campo])
                except:
                    json_data[campo] = np.nan
        return json_data

    def check_fields_type_lista(self, json_data, fields_types):
        """
        Elimina las filas del JSON cuyos elementos en cada campo no sean del tipo especificado en fields_types.
        
        Parámetros:
        - json_data: Diccionario que representa el JSON.
        - fields_types: Diccionario que especifica el tipo esperado para cada campo. Las claves deben ser los nombres de los campos.
        """
        new_json_data = {}
    
        for campo, tipo_esperado in fields_types.items():
            if campo in json_data:
                new_json_data[campo] = []
    
                if not isinstance(json_data[campo], (list, tuple)):
                    json_data[campo] = [json_data[campo]]
    
                for value in json_data[campo]:
                    try:
                        if tipo_esperado == datetime:
                            new_json_data[campo].append(pd.to_datetime(value))
                        else:
                            new_json_data[campo].append(tipo_esperado(value))
                    except:
                        new_json_data[campo].append(np.nan)
    
        return new_json_data