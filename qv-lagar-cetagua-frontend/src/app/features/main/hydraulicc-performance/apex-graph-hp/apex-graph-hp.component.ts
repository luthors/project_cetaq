import { Component, OnInit, ViewChild } from '@angular/core';
import {
  ApexAxisChartSeries,
  ApexChart,
  ApexDataLabels,
  ApexFill,
  ApexGrid,
  ApexLegend,
  ApexMarkers,
  ApexStroke,
  ApexTitleSubtitle,
  ApexXAxis,
  ApexYAxis,
  ChartComponent,
} from 'ng-apexcharts';
import { ChartOptionsHP } from 'src/app/core/models/interfaces/apex-graphs-interfaces';
import { HydraulicPerformanceService } from '../../../../core/services/hydraulic-performance.service';
import { HPExpectedVariables } from 'src/app/core/models/interfaces/hydraulic-performance-response';
import { marker, tooltip } from 'leaflet';
import { JsonPipe } from '@angular/common';
import { MAX_ITEMS_GRAPH } from 'src/environments/environment';

@Component({
  selector: 'app-apex-graph-hp',
  templateUrl: './apex-graph-hp.component.html',
  styleUrls: ['./apex-graph-hp.component.scss'],
})
export class ApexGraphHpComponent implements OnInit {
  @ViewChild('chartHP') chartHP!: ChartComponent;
  public chartHPOptions!: ChartOptionsHP;

  constructor(private hydraulicService: HydraulicPerformanceService) {}
  ngOnInit(): void {
    this.chartHPOptions = this.initChartHPOptions();
  }

  public loadGraph(sector: any) {
    this.hydraulicService
      .findHydraulicPerformanceBySector(sector)
      .subscribe(data => {
        const dataSource = data;
        this.updateChartHPOptions(dataSource);
      });
  }

  public updateChartHPOptions(dataSource: any) {
    let seriesDataHP = [];
    let seriesDataHPExpected = [];
    let axisXCategories = [];
    // {
    //   x: '01 - 2023',
    //   y: 0,
    //   meta: {
    //     hp_var1: 201,
    //     hp_var2: 202,
    //     hp_var3: 203,
    //   },
    // },
    for (let bimester in dataSource[0]) {
      if (+bimester >= MAX_ITEMS_GRAPH) break;
      let y = dataSource[0][bimester].hp_total_percentage;
      let x =
        dataSource[0][bimester].bimester.toString() +
        ' - ' +
        dataSource[0][bimester].year;
      let meta = {
        contract_number: dataSource[1][bimester].contract_number,
        liters_supplied: dataSource[1][bimester].liters_supplied,
        percentage_adjustment: dataSource[1][bimester].percentage_adjustment,
        percentage_telereading: dataSource[1][bimester].percentage_telereading,
      };
      axisXCategories.push(
        dataSource[0][bimester].bimester.toString() +
          ' - ' +
          dataSource[0][bimester].year
      );
      seriesDataHP.push({ x: x, y: y, meta: meta });
      if (+bimester === dataSource[0].length - 1) {
        let dayExpected = dataSource[0][bimester].bimester + 0.5;
        let yearExpected = dataSource[0][bimester].year;
        if (dayExpected > 6) {
          dayExpected = 0.5;
          yearExpected++;
        }

        axisXCategories.push(dayExpected.toString() + ' - ' + yearExpected);
      }
    }
    let z = {
      x: axisXCategories[axisXCategories.length - 1],
      y: dataSource[2].hp_expected,
    };
    this.chartHP.updateSeries([
      {
        data: seriesDataHP,
      },
    ]);
    this.chartHP.updateOptions({
      xaxis: {
        categories: axisXCategories,
      },
      tooltip: {
        y: {
          formatter: function (val: any, e: any) {
            if (e.dataPointIndex > e.series[0].length - 1) {
              let res = `
              <div>Rendimiento hidraulico Esperado (%)<strong>${dataSource[2].hp_expected}</strong> </div>
              <div>Suministrado esperado (L)<strong>${dataSource[2].supplied_expected}</strong> </div>
              <div>Registrado esperado (L)<strong>${dataSource[2].registed_expected}</strong> </div>
              `;
              return res;
            }
            let res = `
            <div> ${
              e.w.globals.seriesNames[0]
            }  <strong> ${val} </strong> </div> <hr>
            <div> Número de contrato: <strong> ${
              e.w.config.series[0].data[e.dataPointIndex].meta.contract_number
            } </strong> </div>
            <div> Litros suministrados: <strong> ${
              e.w.config.series[0].data[e.dataPointIndex].meta.liters_supplied
            } </strong> </div>
            <div> Porcentaje de ajuste: <strong> ${
              e.w.config.series[0].data[e.dataPointIndex].meta
                .percentage_adjustment
            } </strong> </div>
            <div> Porcentaje de lectura de teléfono: <strong> ${
              e.w.config.series[0].data[e.dataPointIndex].meta
                .percentage_telereading
            } </strong> </div>
            `;
            return res;
          },
        },
      },
    });
    this.chartHP.clearAnnotations();
    this.chartHP.addPointAnnotation({
      x: axisXCategories[axisXCategories.length - 1],
      y: dataSource[2].hp_expected,
      tooltip: {
        title: 'HP esperado',
        text: 'HP esperado',
        marker: {
          show: false,
        },
      },
      label: {
        borderColor: '#00E396',
        style: {
          color: '#fff',
          background: '#00E396',
        },
        text: 'RH esperado',
        orientation: 'vertical',
      },
      marker: {
        size: 8,
        fillColor: '#00E396',
        strokeColor: 'green',
        radius: 2,
      },
    });
  }

  public initChartHPOptions(): ChartOptionsHP {
    return {
      series: [
        {
          name: 'Rendimiento hidraulico (%)',
          data: [
            {
              x: '01 - 2023',
              y: 0,
            },
            {
              x: '02 - 2023',
              y: 5,
            },
            {
              x: '03 - 2023',
              y: 10,
            },
            {
              x: '04 - 2023',
              y: 15,
            },
            {
              x: '05 - 2023',
              y: 20,
            },
            {
              x: '06 - 2023',
              y: 25,
            },
          ],
        },
        {
          name: 'Rendimiento hidraulico esperado (%)',
          data: [],
        },
      ],
      chart: {
        height: 350,
        type: 'line',
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        width: 5,
        curve: 'straight',
        dashArray: [0, 8, 5],
      },
      title: {
        text: '',
        align: 'left',
      },
      legend: {
        tooltipHoverFormatter: function (val: any, opts: any) {
          return (
            val +
            ' - <strong>' +
            opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] +
            '</strong>'
          );
        },
      },
      markers: {
        size: 0,
        hover: {
          sizeOffset: 6,
        },
      },
      xaxis: {
        labels: {
          trim: false,
        },
        categories: [
          '01 - 2023',
          '02 - 2023',
          '03 - 2023',
          '04 - 2023',
          '05 - 2023',
          '06 - 2023',
        ],
        tickPlacement: 'between',
      },
      tooltip: {
        hideEmptySeries: true,
        enabledOnSeries: [0],
        y: {
          title: {
            formatter: function (val: any, e: any) {
              return '';
            },
          },
          formatter: function (val: any, e: any) {
            if (e.dataPointIndex > e.series[0].length - 1) {
              return '';
            }
            return val;
          },
        },
      },
      grid: {
        borderColor: '#f1f1f1',
      },
      yaxis: {
        min: 0,
        max: 100,
      },
      colors: [],
      fill: {},
    };
  }
}
