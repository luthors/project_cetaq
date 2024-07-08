export interface AnomalyResponse {
  flow?: DailyVolume; // Caudal
  minFlow?: DailyVolume; // Caudal minimo
  dailyVolume?: DailyVolume; // Volumen diario
  pressure?: DailyVolume; // Presion media
  minFlowMultmeanFlow?: DailyVolume; // Caudal minimo por volumen medio
  minFlowDivmeanFlow?: DailyVolume; // Caudal minimo por volumen medio
  meteo?: Meteo;
  AnomalousDays?: AnomalousDays;
}

export interface AnomalousDays {
  datetime: Date[];
  anomaly: number[];
}

export interface DailyVolume {
  datetime?: Date[];
  data?: number[];
  anomaly?: number[];
  meanSurrounding?: number[];
}

export interface Meteo {
  datetime: Date[];
  precipitation: number[];
  temperature: number[];
}
