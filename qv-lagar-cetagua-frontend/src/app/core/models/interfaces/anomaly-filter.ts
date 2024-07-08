export interface AnomalyFilterRequest {
  anomaly_filter_full: AnomalyFilterFull;
  anomaly_filter: AnomalyFilter;
}

export interface AnomalyFilter {
  number_of_days: number;
  tolerance: ToleranceFilter;
  indicator_number: number;
  sector: number;
}

export enum ToleranceFilter {
  low = 'BAJA',
  medium = 'MEDIA',
  high = 'ALTA',
}
export interface AnomalyFilterFull {
  flow: Flow;
  minFlow: DailyVolume;
  dailyVolume: DailyVolume;
  pressure: MinFlowDivmeanFlow;
  minFlowMultmeanFlow: MinFlowDivmeanFlow;
  minFlowDivmeanFlow: MinFlowDivmeanFlow;
  meteo: Meteo;
}

export interface DailyVolume {
  active: boolean;
  movingAverageDays: number;
  fixedAverageDays: number;
  weightAverage: number;
  weightDeviation: number;
  tolerance: number;
}

export interface Flow {
  active: boolean;
  meanWeekDays: number;
  meanSurrounding: number;
  hours: number;
  tolerance: number;
}

export interface Meteo {
  active: boolean;
}

export interface MinFlowDivmeanFlow {
  active: boolean;
  movingAverageDays: number;
  weightAverage: number;
  weightDeviation: number;
}
