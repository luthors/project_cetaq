from typing import Any
from dataclasses import dataclass
import json
@dataclass
class DailyVolume:
    active: bool
    movingAverageDays: int
    fixedAverageDays: int
    weightAverage: int
    weightDeviation: float
    tolerance: float

    @staticmethod
    def from_dict(obj: Any) -> 'DailyVolume':
        _active = bool(obj.get("active"))
        _movingAverageDays = int(obj.get("movingAverageDays"))
        _fixedAverageDays = int(obj.get("fixedAverageDays"))
        _weightAverage = int(obj.get("weightAverage"))
        _weightDeviation = float(obj.get("weightDeviation"))
        _tolerance = float(obj.get("tolerance"))
        return DailyVolume(_active, _movingAverageDays, _fixedAverageDays, _weightAverage, _weightDeviation, _tolerance)

@dataclass
class Flow:
    active: bool
    meanWeekDays: int
    hours: int
    tolerance: float

    @staticmethod
    def from_dict(obj: Any) -> 'Flow':
        _active = bool(obj.get("active"))
        _meanWeekDays = int(obj.get("meanWeekDays"))
        _hours = int(obj.get("hours"))
        _tolerance = float(obj.get("tolerance"))
        return Flow(_active, _meanWeekDays, _hours, _tolerance)

@dataclass
class Meteo:
    active: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Meteo':
        _active = bool(obj.get("active"))
        return Meteo(_active)

@dataclass
class MinFlow:
    active: bool
    movingAverageDays: int
    fixedAverageDays: int
    weightAverage: int
    weightDeviation: float
    tolerance: float

    @staticmethod
    def from_dict(obj: Any) -> 'MinFlow':
        _active = bool(obj.get("active"))
        _movingAverageDays = int(obj.get("movingAverageDays"))
        _fixedAverageDays = int(obj.get("fixedAverageDays"))
        _weightAverage = int(obj.get("weightAverage"))
        _weightDeviation = float(obj.get("weightDeviation"))
        _tolerance = float(obj.get("tolerance"))
        return MinFlow(_active, _movingAverageDays, _fixedAverageDays, _weightAverage, _weightDeviation, _tolerance)

@dataclass
class MinFlowDivmeanFlow:
    active: bool
    movingAverageDays: int
    weightAverage: int
    weightDeviation: float

    @staticmethod
    def from_dict(obj: Any) -> 'MinFlowDivmeanFlow':
        _active = bool(obj.get("active"))
        _movingAverageDays = int(obj.get("movingAverageDays"))
        _weightAverage = int(obj.get("weightAverage"))
        _weightDeviation = float(obj.get("weightDeviation"))
        return MinFlowDivmeanFlow(_active, _movingAverageDays, _weightAverage, _weightDeviation)

@dataclass
class MinFlowMultmeanFlow:
    active: bool
    movingAverageDays: int
    weightAverage: int
    weightDeviation: float

    @staticmethod
    def from_dict(obj: Any) -> 'MinFlowMultmeanFlow':
        _active = bool(obj.get("active"))
        _movingAverageDays = int(obj.get("movingAverageDays"))
        _weightAverage = int(obj.get("weightAverage"))
        _weightDeviation = float(obj.get("weightDeviation"))
        return MinFlowMultmeanFlow(_active, _movingAverageDays, _weightAverage, _weightDeviation)

@dataclass
class Pressure:
    active: bool
    movingAverageDays: int
    weightAverage: int
    weightDeviation: float

    @staticmethod
    def from_dict(obj: Any) -> 'Pressure':
        _active = bool(obj.get("active"))
        _movingAverageDays = int(obj.get("movingAverageDays"))
        _weightAverage = int(obj.get("weightAverage"))
        _weightDeviation = float(obj.get("weightDeviation"))
        return Pressure(_active, _movingAverageDays, _weightAverage, _weightDeviation)


@dataclass
class Parameters:
    flow: Flow
    minFlow: MinFlow
    dailyVolume: DailyVolume
    pressure: Pressure
    minFlowMultmeanFlow: MinFlowMultmeanFlow
    minFlowDivmeanFlow: MinFlowDivmeanFlow
    meteo: Meteo
    
    @staticmethod
    def from_dict(obj: Any) -> 'Parameters':
        _flow = Flow.from_dict(obj.get("flow"))
        _minFlow = MinFlow.from_dict(obj.get("minFlow"))
        _dailyVolume = DailyVolume.from_dict(obj.get("dailyVolume"))
        _pressure = Pressure.from_dict(obj.get("pressure"))
        _minFlowMultmeanFlow = MinFlowMultmeanFlow.from_dict(obj.get("minFlowMultmeanFlow"))
        _minFlowDivmeanFlow = MinFlowDivmeanFlow.from_dict(obj.get("minFlowDivmeanFlow"))
        _meteo = Meteo.from_dict(obj.get("meteo"))
        return Parameters(_flow, _minFlow, _dailyVolume, _pressure, _minFlowMultmeanFlow, _minFlowDivmeanFlow, _meteo)

@dataclass
class Root:
    Parameters: Parameters

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _Parameters = Parameters.from_dict(obj.get("Parameters"))
        return Root(_Parameters)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)