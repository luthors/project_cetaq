import { Component, OnInit, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { AnomalyService } from 'src/app/core/services/anomaly.service';
import {
  AnomalousDays,
  AnomalyResponse,
  DailyVolume,
  Meteo,
} from 'src/app/core/models/interfaces/anomaly-response';
import {
  ChartOptionsAnomalous,
  ChartOptionsCommonAnomalous,
} from 'src/app/core/models/interfaces/apex-graphs-interfaces';

@Component({
  selector: 'app-apex-graph-defects',
  templateUrl: './apex-graph.component.html',
  styleUrls: ['./apex-graph.component.scss'],
})
export class ApexGraphComponent implements OnInit {
  public chartFlowOptions!: ChartOptionsAnomalous;
  public chartMinFlowOptions!: ChartOptionsAnomalous;
  public chartDailyVolumeOptions!: ChartOptionsAnomalous;
  public chartPressureOptions!: ChartOptionsAnomalous;
  public chartMinFlowMultmeanFlowOptions!: ChartOptionsAnomalous;
  public chartMinFlowDivmeanFlowOptions!: ChartOptionsAnomalous;
  public chartMeteoOptions!: ChartOptionsAnomalous;
  public chartCommonOptions: ChartOptionsCommonAnomalous = {
    dataLabels: {
      enabled: false,
    },
    toolbar: {
      tools: {
        selection: true,
      },
    },
    markers: {
      size: 5,
      hover: {
        size: 10,
      },
    },
    annotations: {},
    tooltip: {
      followCursor: false,
      theme: 'light',
      x: {
        show: false,
      },
      marker: {
        show: false,
      },
      y: {
        title: {
          formatter: function (value: any) {
            return '';
          },
        },
        formatter: function (value: number) {
          return value.toFixed(2);
        },
      },
    },
    grid: {
      padding: {
        top: -20,
        right: 5,
        bottom: -5,
        left: 5,
      },
    },
    xaxis: {
      type: 'datetime',
      labels: {
        show: false,
      },
      tickPlacement: 'between',
    },
  };

  @ViewChild('chartMinFlow') chartMinFlow!: ChartComponent;
  @ViewChild('chartMeteo') chartMeteo!: ChartComponent;
  @ViewChild('chartDailyVolume') chartDailyVolume!: ChartComponent;
  @ViewChild('chartPressure') chartPressure!: ChartComponent;
  @ViewChild('chartMinFlowMultmeanFlow')
  chartMinFlowMultmeanFlow!: ChartComponent;
  @ViewChild('chartMinFlowDivmeanFlow')
  chartMinFlowDivmeanFlow!: ChartComponent;
  @ViewChild('chartFlow') chartFlow!: ChartComponent;
  dataResponse!: AnomalyResponse;
  // @ViewChild('charCommon')
  // charCommon!: ChartComponent;
  constructor(private anomalyService: AnomalyService) {}
  ngOnInit(): void {
    this.chartFlowOptions = this.initChartFlowOptions();
    this.chartPressureOptions = this.initChartPressureOptions();
    this.chartMinFlowOptions = this.initChartMinFlowOptions();
    this.chartDailyVolumeOptions = this.initChartDailyVolumeOptions();
    this.chartMeteoOptions = this.initChartMeteoOptions();
    this.chartMinFlowMultmeanFlowOptions =
      this.initChartMinFlowMultmeanFlowOptions();
    this.chartMinFlowDivmeanFlowOptions =
      this.initChartMinFlowDivmeanFlowOptions();
  }

  public loadGraph(dataHttp: any, parametros: any): void {
    this.chartFlow.clearAnnotations();
    this.chartMinFlowDivmeanFlow.clearAnnotations();
    this.chartMinFlowMultmeanFlow.clearAnnotations();
    this.chartDailyVolume.clearAnnotations();
    this.chartMeteo.clearAnnotations();
    this.chartPressure.clearAnnotations();
    this.chartMinFlow.clearAnnotations();
    this.dataResponse = dataHttp as AnomalyResponse;
    if (this.dataResponse === undefined || this.dataResponse === null) {
      return;
    }
    const anomalousDays: AnomalousDays = this.dataResponse.AnomalousDays!;
    this.paintAnnotations(anomalousDays); //this.chartCommonOptions.annotations =

    const minFlow: DailyVolume = this.dataResponse.minFlow!;
    this.updateChartMinFlowOptions(minFlow);

    const dailyVolume: DailyVolume = this.dataResponse.dailyVolume!;
    this.updateChartDailyVolumeOptions(dailyVolume);

    const pressure: DailyVolume = this.dataResponse.pressure!;
    this.updateChartPressureOptions(pressure);

    const meteo: Meteo = this.dataResponse.meteo!;
    this.updateChartMeteoOptions(meteo);

    const minFlowMultmeanFlow: DailyVolume =
      this.dataResponse.minFlowMultmeanFlow!;
    this.updateChartMinFlowMultmeanFlowOptions(minFlowMultmeanFlow);

    const minFlowDivmeanFlow: DailyVolume =
      this.dataResponse.minFlowDivmeanFlow!;
    this.updateChartMinFlowDivmeanFlowOptions(minFlowDivmeanFlow);
    console.log(parametros);
    let tolerance = parametros.flow.tolerance as number || 0.5;
    const flow: DailyVolume = this.dataResponse.flow!;
    this.updateChartFlowOptions(tolerance, flow);


  }
  public updateChartFlowOptions(tolerance: number, flow?: DailyVolume): void {
    if (flow === undefined) {
      console.log('flow is undefined');
      return;
    }
    console.log('continue flow is not undefined');

    let lineData = [];
    let rangeData = [];

    for (let day in flow.datetime) {
      let date = flow.datetime![parseInt(day)];
      let isAnomaly = flow.anomaly![parseInt(day)];
      let x = new Date(date).getTime();
      let y = flow.data![parseInt(day)];
      let meanSurrounding = flow.meanSurrounding![parseInt(day)];
      let topSurround = meanSurrounding * (1 + tolerance);
      let buttonSurround = meanSurrounding * (1 - tolerance);
      let itemSurroundRange = { x: x, y: [buttonSurround, topSurround] };
      let itemLineSurround = { x: x, y: y };

      rangeData.push(itemSurroundRange);
      lineData.push(itemLineSurround);
      if (parseInt(day) % 24 !== 0 && parseInt(day) !== 0) {
        continue;
      }
      if (isAnomaly === 1) {
        this.chartFlow.addPointAnnotation({
          x: x,
          y: y,
          marker: {
            size: 10,
            fillColor: '#dc143c99',
            strokeColor: 'red',
            strokeWidth: 6,
            shape: 'square',
            radius: 2,
            cssClass: 'apexcharts-custom-class',
          },
          label: {
            borderColor: '#FF4560',
            offsetY: 0,
            style: {
              fontSize: '12px',
              color: '#ffffff',
              background: '#dc143c',
              fontWeight: 'bold',
            },
            text: '  ',
          },
        });
      }
    }
    this.chartFlow.updateSeries([
      {
        data: rangeData,
      },
      {
        data: [],
      },
      {
        data: lineData,
      },
    ]);
  }
  public updateChartPressureOptions(pressure?: DailyVolume): void {
    // this.chartPressure.clearAnnotations();
    if (pressure === undefined) {
      console.log('pressure is undefined');
      return;
    }
    let seriesData = [];
    for (let day in pressure.anomaly) {
      let date = pressure.datetime![parseInt(day)];
      let x = new Date(date).getTime();
      let y = pressure.data![parseInt(day)];
      seriesData.push([x, y]);
      let isAnomaly = pressure.anomaly![parseInt(day)];
      if (isAnomaly === 1) {
        this.chartPressure.addPointAnnotation({
          x: x,
          y: y,
          marker: {
            size: 8,
            fillColor: '#dc143c99',
            strokeColor: 'red',
            radius: 2,
            cssClass: 'apexcharts-custom-class',
          },
          label: {
            borderColor: '#FF4560',
            offsetY: 0,
            style: {
              fontSize: '12px',
              color: '#ffffff',
              background: '#dc143c',
              fontWeight: 'bold',
            },
            text: '  ',
          },
        });
      }
    }
    this.chartPressure.updateSeries([
      {
        data: seriesData,
      },
    ]);
  }
  public updateChartMinFlowOptions(minFlow?: DailyVolume): void {
    // this.chartMinFlow.clearAnnotations();
    if (minFlow === undefined) {
      return;
    }
    let seriesData = [];
    for (let day in minFlow.anomaly) {
      let date = minFlow.datetime![parseInt(day)];
      let x = new Date(date).getTime();
      let y = minFlow.data![parseInt(day)];
      seriesData.push([x, y]);
      let isAnomaly = minFlow.anomaly![parseInt(day)];
      if (isAnomaly === 1) {
        this.chartMinFlow.addPointAnnotation({
          x: x,
          y: y,
          marker: {
            size: 8,
            fillColor: '#dc143c99',
            strokeColor: 'red',
            radius: 2,
            cssClass: 'apexcharts-custom-class',
          },
          label: {
            borderColor: '#FF4560',
            offsetY: 0,
            style: {
              fontSize: '12px',
              color: '#ffffff',
              background: '#dc143c',
              fontWeight: 'bold',
            },
            text: '  ',
          },
        });
      }
    }
    this.chartMinFlow.updateSeries([
      {
        data: seriesData,
      },
    ]);
  }
  public updateChartDailyVolumeOptions(dailyVolume?: DailyVolume): void {
    // this.chartDailyVolume.clearAnnotations();
    if (dailyVolume === undefined) {
      return;
    }
    let seriesData = [];
    for (let day in dailyVolume.anomaly) {
      let date = dailyVolume.datetime![parseInt(day)];
      let x = new Date(date).getTime();
      let y = dailyVolume.data![parseInt(day)];
      seriesData.push([x, y]);

      let isAnomaly = dailyVolume.anomaly![parseInt(day)];
      if (isAnomaly === 1) {
        this.chartDailyVolume.addPointAnnotation({
          x: x,
          y: y,
          marker: {
            size: 8,
            fillColor: '#dc143c99',
            strokeColor: 'red',
            radius: 2,
            cssClass: 'apexcharts-custom-class',
          },
          label: {
            borderColor: '#FF4560',
            offsetY: 0,
            style: {
              fontSize: '12px',
              color: '#ffffff',
              background: '#dc143c',
              fontWeight: 'bold',
            },
            text: '  ',
          },
        });
      }
    }
    this.chartDailyVolume.updateSeries([
      {
        data: seriesData,
      },
    ]);
  }
  public updateChartMeteoOptions(meteo?: Meteo): void {
    // this.chartMeteo.clearAnnotations();
    if (meteo === undefined) {
      return;
    }

    let seriesDataLluvia = [];
    let seriesDataTemperatura = [];
    for (let day in meteo.datetime) {
      let date = meteo.datetime![parseInt(day)];
      let x = new Date(date).getTime();
      let y = meteo.precipitation![parseInt(day)]*100;
      let z = meteo.temperature![parseInt(day)];
      seriesDataLluvia.push([x, y]);
      seriesDataTemperatura.push([x, z]);
    }
    this.chartMeteo.updateSeries([
      {
        data: seriesDataLluvia,
      },
      {
        data: seriesDataTemperatura,
      },
    ]);
  }

  public updateChartMinFlowMultmeanFlowOptions(
    minFlowMultMeanFlow?: DailyVolume
  ): void {
    // this.chartMinFlowMultmeanFlow.clearAnnotations();
    if (minFlowMultMeanFlow === undefined) {
      console.log('no ---------------data');
      return;
    }
    let seriesData = [];
    for (let day in minFlowMultMeanFlow.anomaly) {
      let date = minFlowMultMeanFlow.datetime![parseInt(day)];
      let x = new Date(date).getTime();
      let y = minFlowMultMeanFlow.data![parseInt(day)];
      seriesData.push([x, y]);
      let isAnomaly = minFlowMultMeanFlow.anomaly![parseInt(day)];
      if (isAnomaly === 1) {
        this.chartMinFlowMultmeanFlow.addPointAnnotation({
          x: x,
          y: y,
          marker: {
            size: 8,
            fillColor: '#dc143c99',
            strokeColor: 'red',
            radius: 2,
            cssClass: 'apexcharts-custom-class',
          },
          label: {
            borderColor: '#FF4560',
            offsetY: 0,
            style: {
              fontSize: '12px',
              color: '#ffffff',
              background: '#dc143c',
              fontWeight: 'bold',
            },
            text: '  ',
          },
        });
      }
    }

    this.chartMinFlowMultmeanFlow.updateSeries([
      {
        data: seriesData,
      },
    ]);
  }

  public updateChartMinFlowDivmeanFlowOptions(
    minFlowDivMeanFlow?: DailyVolume
  ): void {
    // this.chartMinFlowDivmeanFlow.clearAnnotations();
    if (minFlowDivMeanFlow === undefined) {
      console.log('no ---------------data');
      return;
    }
    let seriesData = [];
    for (let day in minFlowDivMeanFlow.anomaly) {
      let date = minFlowDivMeanFlow.datetime![parseInt(day)];
      let x = new Date(date).getTime();
      let y = minFlowDivMeanFlow.data![parseInt(day)];
      seriesData.push([x, y]);
      let isAnomaly = minFlowDivMeanFlow.anomaly![parseInt(day)];
      if (isAnomaly === 1) {
        this.chartMinFlowDivmeanFlow.addPointAnnotation({
          x: x,
          y: y,
          marker: {
            size: 8,
            fillColor: '#dc143c99',
            strokeColor: 'red',
            radius: 2,
            cssClass: 'apexcharts-custom-class',
          },
          label: {
            borderColor: '#FF4560',
            offsetY: 0,
            style: {
              fontSize: '12px',
              color: '#ffffff',
              background: '#dc143c',
              fontWeight: 'bold',
            },
            text: '  ',
          },
        });
      }
    }
    this.chartMinFlowDivmeanFlow.updateSeries([
      {
        data: seriesData,
      },
    ]);
    if (minFlowDivMeanFlow.data){
      console.log(minFlowDivMeanFlow);
      this.chartMinFlowDivmeanFlow.updateOptions({
        xaxis: {
          min: seriesData[0][0] - 43200000,
          max: seriesData[seriesData.length - 1][0] + 43200000,
        },
      });
    }
  }
  public paintAnnotations(anomalousDays?: AnomalousDays): void {
    this.chartFlow.clearAnnotations();
    this.chartMinFlowMultmeanFlow.clearAnnotations();
    this.chartMinFlowDivmeanFlow.clearAnnotations();
    this.chartDailyVolume.clearAnnotations();
    this.chartMeteo.clearAnnotations();
    this.chartPressure.clearAnnotations();
    this.chartMinFlow.clearAnnotations();
    if (anomalousDays === undefined) {
      return;
    }
    for (let day in anomalousDays.anomaly) {
      let xaxisAnnotationsObject = {
        x: new Date(anomalousDays.datetime[day]).getTime() - 33200000,
        x2: new Date(anomalousDays.datetime[day]).getTime() + 33200000,
        fillColor: '#dc143c33',
        borderColor: '#9c0000',
        opacity: 0.4,
        offsetX: 0,
        offsetY: 0,
        label: {
          borderColor: '#9c0720',
          offsetX: 15,
          offsetY: 0,
          style: {
            fontSize: '10px',
            color: '#ffffff',
            background: '#dc143ccc',
            fontWeight: 'bold',
          },
          text: '',
        },
      };

      let xaxisAnnotationsObjectTitle= {
        x: new Date(anomalousDays.datetime[day]).getTime() - 33200000,
        x2: new Date(anomalousDays.datetime[day]).getTime() + 33200000,
        fillColor: '#dc143c33',
        borderColor: '#9c0000',
        opacity: 0.4,
        offsetX: 0,
        offsetY: 0,
        label: {
          borderColor: '#9c0720',
          offsetX: 15,
          offsetY: 0,
          style: {
            fontSize: '10px',
            color: '#ffffff',
            background: '#dc143ccc',
            fontWeight: 'bold',
          },
          text: 'Día Anómalo',
        },
      };

      if (anomalousDays.anomaly[day] === 1) {
        this.chartFlow.addXaxisAnnotation(xaxisAnnotationsObjectTitle);
        this.chartMinFlow.addXaxisAnnotation(xaxisAnnotationsObject);
        this.chartDailyVolume.addXaxisAnnotation(xaxisAnnotationsObject);
        this.chartPressure.addXaxisAnnotation(xaxisAnnotationsObject);
        this.chartMinFlowMultmeanFlow.addXaxisAnnotation(xaxisAnnotationsObject);
        this.chartMinFlowDivmeanFlow.addXaxisAnnotation(xaxisAnnotationsObject);
        this.chartMeteo.addXaxisAnnotation(xaxisAnnotationsObject);
      }

    }
  }

  public clearAnotations(): void {
    this.chartFlow.clearAnnotations();
    this.chartMinFlow.clearAnnotations();
    this.chartDailyVolume.clearAnnotations();
    this.chartPressure.clearAnnotations();
    this.chartMinFlowMultmeanFlow.clearAnnotations();
    this.chartMinFlowDivmeanFlow.clearAnnotations();
    this.chartMeteo.clearAnnotations();
  }

  public initChartFlowOptions(): ChartOptionsAnomalous {
    return {
      series: [
        {
          name: 'flow',
          type: 'rangeArea',
          data: [
            {
              x: 1695013200000,
              y: [5.85025, 10.86475],
            },
            {
              x: 1695099600000,
              y: [2.6066249999999997, 4.840875],
            },
            {
              x: 1695186000000,
              y: [3.658375, 6.794125],
            },
            {
              x: 1695272400000,
              y: [5.396125, 10.021375],
            },
            {
              x: 1695358800000,
              y: [5.586875, 10.375625000000001],
            },
            {
              x: 1695445200000,
              y: [5.579, 10.361],
            },
            {
              x: 1695531600000,
              y: [6.055266304347826, 11.245494565217392],
            },
          ],
        },

        {
          name: '',
          type: '',
          data: [],
        },

        {
          name: 'Team B Median',
          type: 'line',
          data: [
            {
              x: 1695013200000,
              y: 6.6775,
            },
            {
              x: 1695099600000,
              y: 2.65,
            },
            {
              x: 1695186000000,
              y: 3.63,
            },
            {
              x: 1695272400000,
              y: 7.745,
            },
            {
              x: 1695358800000,
              y: 8.0925,
            },
            {
              x: 1695445200000,
              y: 7.0575,
            },
            {
              x: 1695531600000,
              y: 6.8374999999999995,
            },
          ],
        },
        {
          type: 'line',
          name: 'Team A Median',
          data: [],
        },
      ],

      chart: {
        id: 'chartFlow',
        group: 'anomaly',
        height: 100,
        type: 'rangeArea',
        animations: {
          speed: 500,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ['#f8ff0f33', '#33b2df', '#095c00', '#33b2df'],
      dataLabels: {
        enabled: true,
      },
      fill: {},
      stroke: {
        curve: 'smooth',

        width: 1,
      },
      legend: {
        show: false,
      },
      xaxis: {},
      yaxis: {
        tickAmount: 5,
        showForNullSeries: false,
        labels: {
          show: true,
          formatter: function (val) {
            return val.toFixed(0);
          },
          offsetX: -10,
          offsetY: 0,
          minWidth: 30,
        },
        title: {
          text: 'Caudal',
          style: {
            fontSize: '12px',
            fontWeight: 'bold',
          },
        },
      },
      markers: {
        // hover: {
        //   sizeOffset: 5,
        // },
      },
    };
  }
  public initChartPressureOptions(): ChartOptionsAnomalous {
    return {
      series: [
        {
          name: 'pressure',
          data: this.generateDayWiseTimeSeries(
            new Date('2023-09-18 06:00:00').getTime(),
            7,
            {
              min: 0,
              max: 10,
            }
          ),
        },
      ],
      chart: {
        id: 'chartPressure',
        group: 'anomaly',
        height: '100',
        type: 'line',
        animations: {
          speed: 500,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ['#21eb72'],
      dataLabels: {
        enabled: false,
      },
      fill: {
        opacity: [0.24, 0.24, 1, 1],
      },
      stroke: {
        curve: 'smooth',
        width: 1,
        lineCap: 'square',
      },
      legend: {},
      xaxis: {},
      yaxis: {
        tickAmount: 5,
        showForNullSeries: false,
        labels: {
          show: true,
          formatter: function (val) {
            return val.toFixed(0);
          },
          offsetX: -10,
          offsetY: 0,
          minWidth: 30,
        },
        title: {
          text: 'Presion Med',
          style: {
            fontSize: '12px',
            fontWeight: 'bold',
          },
        },
      },
      markers: {
        // hover: {
        //   sizeOffset: 5,
        // },
      },
    };
  }
  public initChartMinFlowOptions(): ChartOptionsAnomalous {
    return {
      series: [
        {
          name: 'minFlow',
          data: this.generateDayWiseTimeSeries(
            new Date('2023-09-18T06:00:00').getTime(),
            7,
            {
              min: 0,
              max: 10,
            }
          ),
        },
      ],
      chart: {
        id: 'chartMinFlow',
        group: 'anomaly',
        height: 100,
        type: 'line',
        animations: {
          speed: 500,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ['#21eb72'],
      dataLabels: {
        enabled: false,
      },
      fill: {},
      stroke: {
        curve: 'stepline',
        width: 1,
      },
      legend: {},
      xaxis: {},
      yaxis: {
        tickAmount: 5,
        showForNullSeries: false,
        labels: {
          show: true,
          formatter: function (val) {
            return val.toFixed(0);
          },
          offsetX: -10,
          offsetY: 0,
          minWidth: 30,
        },
        title: {
          text: 'Caudal Min',
          style: {
            fontSize: '12px',
            fontWeight: 'bold',
          },
        },
      },
      markers: {
        // hover: {
        //   sizeOffset: 5,
        // },
      },
    };
  }
  public initChartDailyVolumeOptions(): ChartOptionsAnomalous {
    return {
      series: [
        {
          name: 'dailyVolume',
          data: this.generateDayWiseTimeSeries(
            new Date('2023-09-18T06:00:00').getTime(),
            7,
            {
              min: 0,
              max: 10,
            }
          ),
        },
      ],
      chart: {
        id: 'chartDailyVolume',
        group: 'anomaly',
        height: '100',
        type: 'line',
        animations: {
          speed: 500,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ['#21eb72'],
      dataLabels: {
        enabled: false,
      },
      fill: {
        opacity: [0.24, 0.24, 1, 1],
      },
      stroke: {
        curve: 'stepline',
        width: 1,
      },
      legend: {},
      xaxis: {},
      yaxis: {
        tickAmount: 5,
        showForNullSeries: false,
        labels: {
          show: true,
          formatter: function (val) {
            return val.toFixed(0);
          },
          offsetX: -10,
          offsetY: 0,
          minWidth: 30,
        },
        title: {
          text: 'Volumen Diario',
          style: {
            fontSize: '12px',
            fontWeight: 'bold',
          },
        },
      },
      markers: {
        // hover: {
        //   sizeOffset: 5,
        // },
      },
    };
  }
  public initChartMeteoOptions(): ChartOptionsAnomalous {
    return {
      series: [
        {
          name: 'Precipitación',
          data: [
            [1695034800000, 15.0],
            [1695121200000, 13.6],
            [1695207600000, 13.0],
            [1695294000000, 13.4],
            [1695380400000, 10.3],
            [1695466800000, 11.0],
            [1695553200000, 13.9],
          ],
        },
        {
          name: 'Temperatura',
          data: [
            [1695034800000, 24.5],
            [1695121200000, 25.5],
            [1695207600000, 31.2],
            [1695294000000, 29.9],
            [1695380400000, 27.0],
            [1695466800000, 25.0],
            [1695553200000, 32],
          ],
        },
      ],
      chart: {
        id: 'chartMeteo',
        group: 'anomaly',
        height: '120',
        type: 'line',
        animations: {
          speed: 500,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ['blue', 'orange'],
      dataLabels: {
        enabled: false,
      },
      fill: {
        opacity: [0.24, 0.24, 1, 1],
      },
      stroke: {
        curve: 'smooth',
        width: 1,
      },
      legend: {},
      xaxis: {},
      yaxis: {
        tickAmount: 5,
        showForNullSeries: false,
        labels: {
          show: true,
          formatter: function (val) {
            return val.toFixed(0);
          },
          offsetX: -10,
          offsetY: 0,
          minWidth: 30,
        },
        title: {
          text: 'Meteorología',
          style: {
            fontSize: '12px',
            fontWeight: 'bold',
          },
        },
      },
      markers: {
        // hover: {
        //   sizeOffset: 5,
        // },
      },
    };
  }
  public initChartMinFlowMultmeanFlowOptions(): ChartOptionsAnomalous {
    return {
      series: [
        {
          name: 'dailyVolume',
          data: this.generateDayWiseTimeSeries(
            new Date('2023-09-18T06:00:00').getTime(),
            7,
            {
              min: 0,
              max: 10,
            }
          ),
        },
      ],
      chart: {
        id: 'chartDailyVolume',
        group: 'anomaly',
        height: '100',
        type: 'line',
        animations: {
          speed: 500,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ['#21eb72'],
      dataLabels: {
        enabled: false,
      },
      fill: {
        opacity: [0.24, 0.24, 1, 1],
      },
      stroke: {
        curve: 'stepline',
        width: 1,
      },
      legend: {},
      xaxis: {},
      yaxis: {
        tickAmount: 5,
        showForNullSeries: false,
        labels: {
          show: true,
          formatter: function (val) {
            return val.toFixed(0);
          },
          offsetX: -10,
          offsetY: 0,
          minWidth: 30,
        },
        title: {
          text: 'CMin X CMed',
          style: {
            fontSize: '12px',
            fontWeight: 'bold',
          },
        },
      },
      markers: {
        // hover: {
        //   sizeOffset: 5,
        // },
      },
    };
  }
  public initChartMinFlowDivmeanFlowOptions(): ChartOptionsAnomalous {
    return {
      series: [
        {
          name: 'dailyVolume',
          data: this.generateDayWiseTimeSeries(
            new Date('2023-09-18 06:00:00').getTime(),
            7,
            {
              min: 0,
              max: 10,
            }
          ),
        },
      ],
      chart: {
        id: 'chartDailyVolume',
        group: 'anomaly',
        height: '100',
        type: 'line',
        animations: {
          speed: 500,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ['#21eb72'],
      dataLabels: {
        enabled: false,
      },
      fill: {
        opacity: [0.24, 0.24, 1, 1],
      },
      stroke: {
        curve: 'stepline',
        width: 1,
      },
      legend: {},
      xaxis: {
        min: new Date('2023-09-17 00:00:00').getTime() + 43200000,
        max: new Date('2023-09-24 00:00:00').getTime() + 43200000,
        type: 'datetime',
        labels: {
          show: true,
        },
        tickPlacement: 'between',
      },
      yaxis: {
        tickAmount: 3,
        showForNullSeries: false,
        min: 0,
        max: 1,
        labels: {
          show: true,
          formatter: function (val) {
            return val.toFixed(1);
          },
          offsetX: -10,
          offsetY: 0,
          minWidth: 30,
        },
        title: {
          text: 'CMin / CMed',
          style: {
            fontSize: '12px',
            fontWeight: 'bold',
          },
        },
      },
      markers: {
        // hover: {
        //   sizeOffset: 5,
        // },
      },
    };
  }
  public generateDayWiseTimeSeries(
    baseval: number,
    count: number,
    yrange: { min: number; max: number }
  ): any[] {
    let i = 0;
    let series = [];
    while (i < count) {
      var x = baseval;
      var y = Math.random() * (yrange.max - yrange.min + 1) + yrange.min;
      series.push([x, y]);
      baseval += 86400000;
      i++;
    }
    return series;
  }
  public generateDayWiseTimeSeriesMinMax(
    baseval: number,
    count: number,
    yrange: { min: number; max: number }
  ): any[] {
    let i = 0;
    let series = [];
    0;
    while (i < count) {
      var x = baseval;
      var y = [
        Math.random() * (yrange.max - yrange.min + 1) + yrange.min,
        Math.random() * (yrange.max - yrange.min + 1) + yrange.min,
      ];
      series.push([x, y]);
      baseval += 86400000;
      i++;
    }
    return series;
  }
}
