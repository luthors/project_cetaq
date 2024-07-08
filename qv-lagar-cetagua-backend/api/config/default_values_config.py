# Default values for anomaly filter when tolerance is low
A_F_DEFAULT_VALUES_TOLERANCE_LOW =  {
                    "anomaly_filter_full": {
                        "flow": {
                            "active": True,
                            "meanWeekDays": 2,
                            'hours': 2,
                            'tolerance': 0.25
                        },
                        'minFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'fixedAverageDays': 30,
                            'weightAverage': 1,
                            'weightDeviation': 0.7,
                            'tolerance': 0.1
                        },
                        'dailyVolume': {
                            'active': True,
                            'movingAverageDays': 7,
                            'fixedAverageDays': 30,
                            'weightAverage': 1,
                            'weightDeviation': 0.7,
                            'tolerance': 0.1
                        },
                        'pressure': {
                            'active': True,
                            'movingAverageDays': 14,
                            'weightAverage': 1,
                            'weightDeviation': 0.7
                        },
                        'minFlowMultmeanFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'weightAverage': 1,
                            'weightDeviation': 0.7
                        },
                        'minFlowDivmeanFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'weightAverage': 1,
                            'weightDeviation': 0.7
                        },
                        'meteo': {
                            'active': True
                        }
                    },
                    "anomaly_filter": {
                        "number_of_days": 7,
                        "tolerance": "BAJA",
                        "indicator_number": 3,
                        "sector": 0,
                        "map": 0
                    }
                }
# Default values for anomaly filter when tolerance is mid
A_F_DEFAULT_VALUES_TOLERANCE_MID =  {
                    "anomaly_filter_full": {
                        "flow": {
                            "active": True,
                            "meanWeekDays": 2,
                            'hours': 4,
                            'tolerance': 0.5
                        },
                        'minFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'fixedAverageDays': 30,
                            'weightAverage': 1,
                            'weightDeviation': 1.2,
                            'tolerance': 0.25
                        },
                        'dailyVolume': {
                            'active': True,
                            'movingAverageDays': 7,
                            'fixedAverageDays': 30,
                            'weightAverage': 1,
                            'weightDeviation': 1.2,
                            'tolerance': 0.25
                        },
                        'pressure': {
                            'active': True,
                            'movingAverageDays': 7,
                            'weightAverage': 1,
                            'weightDeviation': 1.2
                        },
                        'minFlowMultmeanFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'weightAverage': 1,
                            'weightDeviation': 1.2
                        },
                        'minFlowDivmeanFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'weightAverage': 1,
                            'weightDeviation': 1.2
                        },
                        'meteo': {
                            'active': True
                        }
                    },
                    "anomaly_filter": {
                        "number_of_days": 7,
                        "tolerance": "MEDIA",
                        "indicator_number": 3,
                        "sector": 0,
                        "map": 0
                    }
                }
# Default values for anomaly filter when tolerance is high
A_F_DEFAULT_VALUES_TOLERANCE_HIGH =  {
                    "anomaly_filter_full": {
                        "flow": {
                            "active": True,
                            "meanWeekDays": 2,
                            'hours': 8,
                            'tolerance': 0.75
                        },
                        'minFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'fixedAverageDays': 30,
                            'weightAverage': 1,
                            'weightDeviation': 1.5,
                            'tolerance': 0.35
                        },
                        'dailyVolume': {
                            'active': True,
                            'movingAverageDays': 7,
                            'fixedAverageDays': 30,
                            'weightAverage': 1,
                            'weightDeviation': 1.5,
                            'tolerance': 0.35
                        },
                        'pressure': {
                            'active': True,
                            'movingAverageDays': 14,
                            'weightAverage': 1,
                            'weightDeviation': 1.5
                        },
                        'minFlowMultmeanFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'weightAverage': 1,
                            'weightDeviation': 1.5
                        },
                        'minFlowDivmeanFlow': {
                            'active': True,
                            'movingAverageDays': 7,
                            'weightAverage': 1,
                            'weightDeviation': 1.5
                        },
                        'meteo': {
                            'active': True
                        }
                    },
                    "anomaly_filter": {
                        "number_of_days": 7,
                        "tolerance": "ALTA",
                        "indicator_number": 3,
                        "sector": 0,
                        "map": 0
                    }
                }
