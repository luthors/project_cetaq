import {
  ApexAnnotations,
  ApexAxisChartSeries,
  ApexChart,
  ApexDataLabels,
  ApexFill,
  ApexGrid,
  ApexLegend,
  ApexMarkers,
  ApexStroke,
  ApexTitleSubtitle,
  ApexTooltip,
  ApexXAxis,
  ApexYAxis,
} from 'ng-apexcharts';

export interface ChartOptionsAnomalous {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  dataLabels: ApexDataLabels;
  stroke: ApexStroke;
  xaxis: ApexXAxis;
  yaxis: ApexYAxis;
  markers: ApexMarkers;
  colors: string[];
  fill: ApexFill;
  legend: ApexLegend;
}
export interface ChartOptionsCommonAnomalous {
  dataLabels: ApexDataLabels;
  markers: ApexMarkers;
  xaxis: ApexXAxis;
  grid: any;
  tooltip: any;
  toolbar: any;
  annotations: ApexAnnotations;
}
export interface ChartOptionsHP {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  dataLabels: ApexDataLabels;
  stroke: ApexStroke;
  xaxis: ApexXAxis;
  yaxis: ApexYAxis;
  markers: ApexMarkers;
  colors: string[];
  fill: ApexFill;
  legend: ApexLegend;
  title: ApexTitleSubtitle;
  grid: ApexGrid;
  tooltip: any;
}
