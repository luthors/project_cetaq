import requests
import http.client
from typing import List, Dict, Tuple
import json
import pandas
import numpy

class Aemet():
    #key; Indicativo climatológico de la EMA. Puede introducir varios indicativos separados por comas; código del municipio
    def __init__(self, idema: str, mun_code: str):
        '''

        Parameters
        ----------
        idema : str
            Name or list with the name of the climatological values that are needed.
        mun_code : str
            Desired station code.

        Returns
        -------
        None.

        '''
        try:
            with open("apps/transactions/api/processes/fugas/AEMET/config.json") as json_file:
                config_file = json.load(json_file)
        except FileNotFoundError:
            raise FileNotFoundError("Config file not found.")
            
        self.__key = config_file["raw_data_parameters"]["aemet"]["token"]
        self.__idema = idema
        self.__mun_code = mun_code


    def __concat_url(self, url1: str, url2: str) -> str:

        if url1[-1] == "/":
            url1 = url1[:-1]

        if url2[0] == "/":
            url2 = url2[1:]

        return url1 + "/" + url2

    def __make_request_2(self, url) -> "JSON":
        conn = http.client.HTTPSConnection("opendata.aemet.es")

        headers = {
            'cache-control': "no-cache"
            }

        url_request = "https://opendata.aemet.es/opendata"+url+"?api_key=" + self.__key

        conn.request("GET", url_request, headers=headers)
        res = conn.getresponse()
        data = res.read()

        try:
            data =json.loads(data.decode("utf-8"))
        except:
            data = None

        return data
        


    def __make_request(self, url) -> "JSON":
        '''
        Make the request to opendata.aemet.es given an api url
        '''
        site = "https://opendata.aemet.es/opendata/"
        url_request = self.__concat_url(site, url)

        # Basic info to execute the request
        querystring = {"api_key": self.__key}
        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url_request, headers=headers, params=querystring)

        return response.json()



    def __diary_climatological_values(self, initDate: str, endDate: str) -> Tuple[bool, List[Dict]]:
        '''
        Return a List of dictionaries with the climatological info from initDate until endDate

        @param: initDate -> date string format (YYYY-MM-DD)
        @param: endDate -> date string format (YYYY-MM-DD)

        @return: (bool, List[Dict])
        '''
        url = "/api/valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}/".format(initDate + "T00:00:00UTC", endDate + "T23:59:59UTC", self.__mun_code)

        response_json = self.__make_request_2(url)

        if response_json == None:
            response_json = self.__make_request(url)

        status = response_json["estado"] == 200
        data = None
        metadata = None

        if status:
            #Get data
            url_data = response_json["datos"]
            data = requests.request("GET", url_data)
            data = pandas.DataFrame(data.json())
            data = data[self.__idema].to_dict(orient='records')

            #Get metadata
            url_metadata = response_json["metadatos"]
            metadata = requests.request("GET", url_metadata)
            metadata = metadata.json()

        return status, data, metadata

    def get_climatological_info(self, initDate: str, endDate: str) -> Tuple[bool, Dict[str, float]]:
        '''
        Return a boolean, if true, the request was executed correctly, false there was a problem
        Dictionary where the keys are dates in string format (YYYY-MM-DD) and values are precipitation in m³
        Precipitation values from initDate (includes) to endDate (excludes)

        @param: initDate -> date string format (YYYY-MM-DD)
        @param: endDate -> date string format (YYYY-MM-DD)

        @return: (bool, Dict[str, float])
        '''

        status, data, metadata = self.__diary_climatological_values(initDate, endDate)

        if status:
            for d in data:
                for param in self.__idema:
                    if param != 'fecha':
                        try:
                            d[param] = float((d[param]).replace(",", "."))
                        except:
                            d[param] = numpy.nan

        return status, data

    # def get_precipitation_info(self, date: str) -> Tuple[bool, float]:
    #     '''
    #     Return a boolean, if true, the request was executed correctly, false there was a problem
    #     float number representing precipitation for date in m³

    #     @param: date -> date string format (YYYY-MM-DD)

    #     @return: (bool, float)
    #     '''
    #     status, data, metadata = self.__diary_climatological_values(date, date)

    #     precipitation = None

    #     if status:
    #         precipitation = float((data[0]["prec"]).replace(",", "."))

    #     return status, precipitation

    def get_current_prediction(self) -> Tuple[bool, List[Dict]]:

        url = "/api/prediccion/especifica/municipio/diaria/{}".format(self.__mun_code)
        response = self.__make_request(url)

        #Get data
        response_json = response.json()

        url_data = response_json["datos"]
        data = requests.request("GET", url_data)

        #Get metadata
        url_metadata = response_json["metadatos"]
        metadata = requests.request("GET", url_metadata)

        #Ahora mismo devuelve el estado de la operacion, los datos en json y los metadatos
        return (response_json["estado"] == 200), data.json(), metadata.json()
