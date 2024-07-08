import os
import sys
import copy
import json
import pandas as pd
import geopandas as gpd

from shapely import MultiPolygon
from shapely.ops import unary_union


from apps.transactions.api.processes.errores.class_Errores import Errores


DISTANCIA = 25

class Match:

    def __init__(self,excel_contratos,sectores_geojson,acometidas_geojson):
        """
        Para poder realizar comprobaciones, son necesarios tres ficheros:
            - Un excel con los datos de los contratos, la acometida y el sector al que están ligados
            - Un archivo geojson con la geometría de las acometidas
            - Un archivo geojson con los polígonos que conformas los sectores
        
        """
        self.errores = []
       #Entre ambos asteriscos se leen las rutas, se comprueba el tipo de archivo y se pasa a dataframe y geodataframe respectivamente
        error = Errores.file_format(Errores, excel_contratos, '.xlsx')
        if error != True:
            self.errores.append(error)
            return None
        error=Errores.file_format(Errores, sectores_geojson, '.geojson')
        if error is not True:
            self.errores.append(error)
            return None
        error=Errores.file_format(Errores, acometidas_geojson, '.geojson')
        if error is not True:
            self.errores.append(error)
            return None
        self.df_contratos = pd.read_excel(excel_contratos)
        self.gdf_sectores = gpd.read_file(sectores_geojson)
        self.gdf_acometidas = gpd.read_file(acometidas_geojson)
        #
        self._errores_()
        self.gdf_geometrico = gpd.sjoin(self.gdf_acometidas, self.gdf_sectores, how='left', predicate='intersects')
        self.gdf_geometrico['Problemas'] = ''
        self.gdf_geometrico['Sugerencias'] = '' #Creamos la columna para anotar las sugerencias propuestas

        if 'geometry' not in self.gdf_sectores:
            raise ValueError("El archivo de sectores debe contener una columna 'geometry' con objetos geométricos.")
        if 'geometry' not in self.gdf_acometidas:
            raise ValueError("El archivo de acometidas debe contener una columna 'geometry' con objetos geométricos.")

        # except Exception as e:
        #     print(f"Ocurrió un error al leer los ficheros de entrada: {e}")
        #     print("\nPor favor, compruebe que el número de ficheros es adecuado y los ficheros tienen el formato deseado.")

    def _errores_(self):
        """
        Checkea que los archivos tengan la columnas necesarias y con el nombre adecuado. Se usan otras variables para evitar que sobreescriba las originales.ç
        Se realizan copies para no modificar los elementos originales
        """

        df_contratos = copy.deepcopy(self.df_contratos)
        gdf_sectores = copy.deepcopy(self.gdf_sectores)
        gdf_acometidas = copy.deepcopy(self.gdf_acometidas)

        error = Errores.check_columns(Errores, df_contratos, ['Sector', 'ESTADO CONTRATO', 'ID Acometida'])
        if error is not True:
            self.errores.append(error)
            return None
        tipos = {
        'Sector' : str,
        'ESTADO CONTRATO' : str,
        'ID Acometida' : int,
        }
        Errores.check_columns_type(Errores, df_contratos, tipos)      

        error=Errores.check_columns(Errores, gdf_sectores, ['ST_ID', 'ST_NOMBRE'])
        if error is not True:
            self.errores.append(error)
            return None
        
        tipos = {
            'ST_ID' : str,
            'ST_NOMBRE' : str,
            'geometry': type(MultiPolygon),
            }
        
        Errores.check_columns_type(Errores, gdf_sectores, tipos)

        error=Errores.check_columns(Errores, gdf_acometidas, ['GNR_TXT3'])
        if error is not True:
            self.errores.append(error)
            return None
        
        tipos = {
            'GNR_TXT3' : str,
            'geometry': type(MultiPolygon),
            }
        
        Errores.check_columns_type(Errores, gdf_acometidas, tipos)
        
    def dataframe_to_geojson(self,df, output_filename):
        """
        Convierte un DataFrame en un GeoDataFrame y lo guarda en la carpeta output.
        Entrada : DataFrame y nombre del archivo 
        """
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        gdf.to_file('rest_api_cetaqua/files/store/file/'+output_filename, driver='GeoJSON', encoding='utf-8')
    
    def dataframe_to_csv(self,df, output_path):
        """
        Convierte un DataFrame en un CSV y lo guarda en la carpeta output.
        Entrada : DataFrame y nombre del archivo 
        """

        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        gdf.to_csv(output_path)

    def dict_to_json(self,dic, output_path):
        """
        Convierte un Diccionario en un JSON y lo guarda en la carpeta output.
        Entrada : Diccionario y nombre del archivo 
        """
        with open(output_path, 'w') as archivo_json:
            json.dump(dic, archivo_json, indent=2)

    def calculate_pct(self):
        """
        Calcula el porcentaje de errores y del tipo de error total. La información se devuelve en un diccionario
        Errores = set(ID_err)/set(ID_contratado)
        Tipo de error = col(Problemas)/totales
        """
        acometidas_contratadas = len(self.df_contratos['ID Acometida'].unique())
        acometidas_erroneas = len(self.merged.loc[self.merged['Problemas'].notnull(), 'ID Acometida'].unique())
        
        df_unique = self.merged.drop_duplicates(subset=['ID Acometida'])
        mask1 = df_unique['ID Acometida'].unique()

        filtered_data = df_unique.loc[df_unique['ID Acometida'].isin(mask1)]
        self.dataframe_to_csv(filtered_data, 'rest_api_cetaqua/files/store/file/filtered_data.csv')
        
        mask2 = filtered_data['Problemas'].str.contains('Sectores no parejos')
        sect_dup = len(filtered_data.loc[mask2])
        
        mask2 = filtered_data['Problemas'].str.contains('Sectores no definidos')
        sect_no_def = len(filtered_data.loc[mask2])
        
        mask2 = filtered_data['Problemas'].str.contains('Falta sector')
        falta_sect = len(filtered_data.loc[mask2])
        
        # Aplicar la máscara 'Problemas' para filtrar por 'Sectores no parejos'
        mask2 = filtered_data['Problemas'].str.contains('Acometidas duplicadas')
        acom_dup = len(filtered_data.loc[mask2])
        
        dic = {
            "Acometidas Erroneas (%)": round(100*acometidas_erroneas/acometidas_contratadas,2),
            "Acometidas Sectores no parejos (%)": round(100*sect_dup/acometidas_erroneas,2),
            "Acometidas Sectores no definidos (%)": round(100*sect_no_def/acometidas_erroneas,2),
            "Acometidas Falta sector (%)": round(100*falta_sect/acometidas_erroneas,2),
            "Acometidas Acometidas duplicadas (%)": round(100*acom_dup/acometidas_erroneas,2)
        }

        return dic

    
    def _not_match(self):
        """
        Realiza la comparación entre los sectores del dataframe mergeado. Comprueba que el sector que se va a analizar está presente entre los sectores GIS.
        Output -> Sectores no parejos: El ID de sectores de contratos no existe en los sectores GIS disponibles
        """
        mask_not_match = self.merged['Sector GIS'] != self.merged['Sector Contratos']
        mask_not_sector = ~self.merged['Sector Contratos'].isin(self.merged['Sector GIS'])
        self.merged.loc[mask_not_match, 'Problemas'] = 'Sectores no parejos: El ID de sectores de contratos no coincide con la posición de las acometidas según los sectores especificados'
        self.merged.loc[mask_not_match, 'Sugerencias'] = self.merged.apply(lambda row: f"Tomar sector GIS, en este caso: {row['Sector GIS']}", axis=1)
        self.merged.loc[mask_not_sector, 'Problemas'] = 'Sectores no definidos: El ID de sectores de contratos no existe en los sectores GIS disponibles'
        self.merged.loc[mask_not_sector, 'Sugerencias'] = 'Crear sector en GIS y añadirlo al archivo sectores'
        

    def _not_match_nan(self):
        """
        Realiza la comparación entre los sectores del dataframe mergeado. Comprueba que el punto se encuentra dentro de algún polígono
        Output -> Falta sector: Punto fuera de los polígonos de los sectores
        """
        mask_nan = pd.isna(self.merged['Sector GIS'])
        self.merged.loc[mask_nan, 'Problemas'] = 'Falta sector: Punto fuera de los polígonos de los sectores'
        self.merged.loc[mask_nan, 'Sugerencias'] = self.merged.apply(lambda row: f"Añadir punto a polígono GIS, se sugiere el polígono de contratos, en este caso: {row['Sector Contratos']}", axis=1)
       
    def _puntos_duplicados(self):
        """
        Busca aquellos puntos con acometidas duplicadas. Se realiza sobre el join de sectores y acometidas
        Output -> Acometidas duplicadas: Un mismo ID de acometida tiene varios puntos geométricos asociados
        """
        
        centros = self.merged.groupby('ID Acometida')['geometry'].apply(lambda x: unary_union(x.tolist()).centroid)

        # Crear los círculos alrededor de los centros
        círculos = centros.buffer(25)

        # Verificar si todos los puntos de cada grupo caen dentro del círculo
        mask = self.merged.groupby('ID Acometida')['geometry'].apply(lambda x: all(x.within(círculos.loc[x.name])))

        # Agregar los mensajes en la columna 'sugerencia'
       
        for group, circle in círculos.items():
            mask = self.merged['ID Acometida'] == group
            if len(self.merged[mask]) > 1:
                if all(self.merged[mask]['geometry'].within(circle)):
                    self.merged.loc[mask, 'Problemas'] = 'Acometidas duplicadas: Un mismo ID de acometida tiene varios puntos geométricos asociados'
                    self.merged.loc[mask, 'Sugerencias'] = f'Distancia menor de {DISTANCIA} metros, unificar en AQUACIS'
                else:
                    self.merged.loc[mask, 'Problemas'] = 'Acometidas duplicadas: Un mismo ID de acometida tiene varios puntos geométricos asociados'
                    self.merged.loc[mask, 'Sugerencias'] = f'Distancia mayor de {DISTANCIA} metros, comprobar en GIS y AQUACIS'
        

    def _limpiar_obj(self):
        """
        Limpia los inputs para que las columnas tengan el nombre deseado
        """
        self.gdf_geometrico = self.gdf_geometrico.rename(columns={'GNR_TXT3': 'ID Acometida',
                                                                  'ST_ID' : 'Sector GIS'})
        self.df_contratos = self.df_contratos.rename(columns={'Sector': 'Sector Contratos'})
        self.df_contratos = self.df_contratos[self.df_contratos['ESTADO CONTRATO'] == 'CONTRATADO']
        self.df_contratos['ID Acometida'] = self.df_contratos['ID Acometida'].astype(str)
        self.df_contratos =  self.df_contratos[['ID Acometida', 'Sector Contratos']]

        self.gdf_geometrico =  self.gdf_geometrico[['ID Acometida', 'Sector GIS','geometry']]
        self.gdf_geometrico =  self.gdf_geometrico.replace('PARQUE 28 FEBRERO','PARQUE 28 DE FEBRERO')
        self.gdf_geometrico =  self.gdf_geometrico.replace('STA. TERESA','SANTA TERESA')
        self.gdf_geometrico =  self.gdf_geometrico.replace('PTS ARMILLA','SECTOR PTS ARMILLA')
        

    def comprobar_archivos(self):
        """
        Función principal que se encarga de realizar la mayoría del código y devuelve el df resultante y un diccionario con porcentajes de los errores
        """
        self._limpiar_obj()
        self.merged = self.gdf_geometrico.merge(self.df_contratos, on='ID Acometida', how='inner')
        self.merged = self.merged.drop_duplicates()
        self._puntos_duplicados()
        self._not_match() #Anotamos los sectores que no dan merge
        self._not_match_nan()
        #Nos quedamos unicamente con aquellos en los que problemas no es nan
        self.merged = self.merged.dropna(subset=['Problemas'])
        self.merged = self.merged[['ID Acometida','geometry','Sector GIS','Sector Contratos','Problemas','Sugerencias']]
        dic = self.calculate_pct()

        return self.merged, dic

