export interface HydraulicPerformanceResponse {
  id?: number;
  sector: number;
  year: number;
  bimester: number;
  hp_total_percentage: number;
  hp_variables?: HPVariables;
  hp_expected_variables?: HPExpectedVariables;
}

export interface HPVariables {
  contract_number?: number;
  liters_supplied?: number;
  percentage_adjustment?: number;
  percentage_telereading?: number;
}
export interface HPExpectedVariables {
  hp_expected?: number;
  supplied_expected?: number;
  registed_expected?: number;
}
