from faker import Faker
import json


class TransactionsFactories:

    def get_parameters(self):
        parameters ={
            "flow": { "active": True, "meanWeekDays": 2, "hours": 4, "tolerance": 0.5 },
            "minFlow": {
                "active": True,
                "movingAverageDays": 7,
                "fixedAverageDays": 14,
                "weightAverage": 1,
                "weightDeviation": 1.2,
                "tolerance": 0.25
            },
            "dailyVolume": {
                "active": True,
                "movingAverageDays": 7,
                "fixedAverageDays": 14,
                "weightAverage": 1,
                "weightDeviation": 1.2,
                "tolerance": 0.25
            },
            "pressure": {
                "active": True,
                "movingAverageDays": 7,
                "weightAverage": 1,
                "weightDeviation": 1.2
            },
            "minFlowMultmeanFlow": {
                "active": True,
                "movingAverageDays": 7,
                "weightAverage": 1,
                "weightDeviation": 1.2
            },
            "minFlowDivmeanFlow": {
                "active": True,
                "movingAverageDays": 7,
                "weightAverage": 1,
                "weightDeviation": 1.2
            },
            "meteo": { "active": True }
            }

       
        
        return parameters

    def get_excel_file_ok(self):
        files = [
            ('File', ('prueba.xlsx', open('/home/oem/Luthors/Cetaqua/archivos de prueba/leaks/prueba.xlsx',
             'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        return files
