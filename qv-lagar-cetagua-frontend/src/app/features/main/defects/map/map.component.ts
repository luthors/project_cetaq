import { Component, AfterViewInit, Input } from '@angular/core';
import * as L from 'leaflet';
import * as proj4 from 'proj4';
import 'proj4leaflet';
import { AnomalyService } from 'src/app/core/services/anomaly.service';
import { MapService } from 'src/app/core/services/map.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent implements AfterViewInit {
  private map: any;
  geojson: any;
  explotationId: number = 0;
  explotationName: string = '';
  mapId: string = '';
  previousLayers: L.Layer[] = [];
  geojsonprueba: any;
  private selectedSector: any;

  @Input() variableHijo: any;

  constructor(
    private mapService: MapService,
    private anomalyService: AnomalyService
  ) {}

  ngAfterViewInit(): void {
    this.initValues(0);
  }

  // Init value function for map.
  //The argument depends on the user authorization.
  initValues(element: number) {
    
    const exploitation = localStorage.getItem('exploitation');  
    this.mapService.getListMap().subscribe(
      data => {
        if(exploitation != null){
          let result  = data.filter((item : any) => {
            return item.exploitation === parseInt(exploitation, 10);
          })
          this.mapId = result[element].id.toString();   
          this.explotationId = parseInt(exploitation);
          this.variableHijo = this.mapId;
          this.infoExploitation();
          this.initMap();
        }
          
      },
      error => {
        console.log('Error with the list map names', error);
      }
    );
  }

  // Init explotaition values function
  infoExploitation() {
    this.mapService.getMap(this.explotationId).subscribe(
      data => {
        this.explotationName = data.name;
      },
      error => {
        console.log('Error with initial map');
      }
    );
  }

  private initMap(): void {
    const crs = new L.Proj.CRS(
      'EPSG:25830',
      '+proj=utm +zone=30 +ellps=GRS80 +units=m +no_defs',
      {
        resolutions: [8192, 4096, 2048, 1024, 512],
        origin: [0, 0],
        bounds: L.bounds([-804289.52, 4383204.8], [988807.52, 6269072.8]),
      }
    );

    // Initialize the map
    this.map = L.map('map', {});

    // Base layer for map display
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(this.map);
    this.addLegend();

    this.loadGeoJson(this.mapId);
  }

  //Style according to the typology of the sector
  private colorSectorGeoJson(type: string): string {
    switch (type) {
      case 'industrial':
        return 'gray';
      case 'ocio':
        return 'cyan';
      case 'residencial':
        return 'orange';
      case 'social':
        return 'green';
      case 'turismo':
        return 'blueviolet';
      case 'unifamilia':
        return 'magenta';
      default:
        return '';
    }
  }

  // Function to add the geojson layer
  loadGeoJson(mapId: string): void {
    this.mapService.getGeoJson(parseInt(mapId)).subscribe(
      geojson => {
        this.geojsonprueba = geojson;
        const newLayer = L.Proj.geoJson(geojson, {
          style: feature => {
            if (!feature) {
              return {
                fillColor: 'b9b4b4',
                color: 'white',
                weight: 1,
                opacity: 1,
                fillOpacity: 0.7,
              };
            }
            const descriptio = feature.properties.Descriptio;

            return {
              fillColor: '#b9b4b4',
              color: this.colorSectorGeoJson(descriptio),
              weight: 1,
              opacity: 1,
              fillOpacity: 0.7,
            };
          },
          onEachFeature: (feature, layer) => {
            layer.bindPopup(feature.properties.Name);
            layer.on('click', () => this.onSectorClick(feature, layer));
          },
        });
        newLayer.addTo(this.map);
        this.previousLayers.push(newLayer);
        this.map.fitBounds(newLayer.getBounds());
      },
      error => {
        console.error('Error loading GeoJSON:', error);
      }
    );
  }

  clearPreviousLayers(): void {
    this.previousLayers.forEach(layer => {
      this.map.removeLayer(layer);
    });

    this.previousLayers = [];
  }

  // Map legend
  addLegend() {
    const legend = new (L.Control.extend({
      options: { position: 'bottomleft' },
    }))();

    legend.onAdd = function (map: L.Map) {
      const div = L.DomUtil.create('div', 'legend');

      div.innerHTML = `
      <div class="legend-box" style="background-color: rgba(255, 255, 255,0.9); border-radius: 5px>
        <div class="legend-content" style="padding: 10px;">
          <h4 style="margin:5px 2px 5px;">Tipología sector</h4>
          <p style="margin:0px;"><span style="display: inline-block; border: gray 2px solid; padding: 5px; border-radius: 2px; margin-left: 2px;"></span> Industrial</p>
          <p style="margin:0px;"><span style="display: inline-block; border: cyan 2px solid; padding: 5px; border-radius: 2px; margin-left: 2px;"></span> Ocio</p>
          <p style="margin:0px;"><span style="display: inline-block; border: orange 2px solid; padding: 5px; border-radius: 2px; margin-left: 2px;"></span> Residencial</p>
          <p style="margin:0px;"><span style="display: inline-block; border: green 2px solid; padding: 5px; border-radius: 2px; margin-left: 2px;"></span> Social</p>
          <p style="margin:0px;"><span style="display: inline-block; border : blueviolet 2px solid; padding: 5px; border-radius: 2px; margin-left: 2px;"></span> Turismo</p>
          <p style="margin:0px;"><span style="display: inline-block; border: magenta 2px solid; padding: 5px; border-radius: 2px; margin-left: 2px;"></span> Unifamilia</p>
          <h4 style="margin:5px 2px 5px;">Estado</h4>
          <p style="margin:0px;"><span style="display: inline-block; background-color: #b9b4b4; padding: 5px; border-radius: 3px; margin-left: 2px;"></span> Normal</p>
          <p style="margin:0px;"><span style="display: inline-block; background-color: red; padding: 5px; border-radius: 3px; margin-left: 2px;"></span> Anomalía</p>
        </div>
      </div>
    `;
      return div;
    };
    legend.addTo(this.map);
  }

  loadAnomaly(mapId: string, sector: string): void {
    this.mapService.getGeoJson(parseInt(mapId)).subscribe(
      geojson => {
        this.geojsonprueba = geojson;
        const newLayer = L.Proj.geoJson(geojson, {
          style: feature => {
            if (!feature) {
              return {
                fillColor: 'b9b4b4',
                color: 'white',
                weight: 1,
                opacity: 1,
                fillOpacity: 0.7,
              };
            }

            const descriptio = feature.properties.Descriptio;
            if (feature.properties.Name === sector) {
              return {
                fillColor: 'red',
                color: this.colorSectorGeoJson(descriptio),
                weight: 1,
                opacity: 1,
                fillOpacity: 0.7,
              };
            }

            return {
              fillColor: '#b9b4b4',
              color: this.colorSectorGeoJson(descriptio),
              weight: 1,
              opacity: 1,
              fillOpacity: 0.7,
            };
          },
          onEachFeature: (feature, layer) => {
            layer.bindPopup(feature.properties.Name);
            layer.on('click', () => this.onSectorClick(feature, layer));
          },
        });
        newLayer.addTo(this.map);
        this.previousLayers.push(newLayer);
        this.map.fitBounds(newLayer.getBounds());
      },
      error => {
        console.error('Error loading GeoJSON:', error);
      }
    );
  }

  sectorZoom() {}

  onSectorClick(feature: any, layer: any): void {
    this.map.fitBounds(layer.getBounds());
  }

  getExplotationId(mapId: string): void {
    this.mapService.getDetailMap(parseInt(mapId)).subscribe(
      data => {
        this.explotationId = data.exploitation;
        this.explotationName = data.name;
      },
      error => {
        console.log('Error with the list map names', error);
      }
    );
  }

  searchAnomaly(mapId: string, sector: string, days: number, dataHttp:any) {
    var anomalyDays: number[] = dataHttp.AnomalousDays.anomaly;
    var anomaly: boolean = this.AtleastOneAnomaly(anomalyDays, days);
    if (anomaly) {
      this.loadAnomaly(mapId, sector);
    } else {
      this.loadGeoJson(mapId);
      Swal.fire(
        '¡Éxito!',
        'No se encuentran anomalías en el sector en base a los días consecutivos seleccionados y la información cargada en el fichero',
        'success'
      );
    }
    return anomaly;
  }

  AtleastOneAnomaly(anomalyArray: number[], days: number): boolean {
    var countOnes = 0;
    for (let i = 0; i < anomalyArray.length; i++) {
      if (anomalyArray[i] === 1) {
        countOnes++;
        if (countOnes >= days) return true;
      } else countOnes = 0;
    }
    return false;
  }
}
