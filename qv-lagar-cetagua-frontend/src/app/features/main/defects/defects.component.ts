import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { FileUploadComponent } from 'src/app/components/file.upload/file.upload.component';
import { FileUploadService } from 'src/app/core/services/file-upload.service';
import { MapService } from 'src/app/core/services/map.service';
import { SectorService } from 'src/app/core/services/sector.service';
import { MapComponent } from './map/map.component';
import {
  ToleranceFilter,
  AnomalyFilterRequest,
} from '../../../core/models/interfaces/anomaly-filter';
import { AnomalyFilterService } from '../../../core/services/anomaly-filter.service';
import { MeasurementVariablesComponent } from './measurement-variables/measurement-variables.component';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import Swal from 'sweetalert2';
import { AnomalyService } from 'src/app/core/services/anomaly.service';
import { AnomalyFilter } from '../../../core/models/interfaces/anomaly-filter';
import { ApexGraphComponent } from './apex-graph-defects/apex-graph.component';
import { InfoCardComponent } from 'src/app/components/info.card/info.card.component';
import { LoaderService } from 'src/app/core/services/loader.service';
import { AuthenticationService } from 'src/app/core/services/authentication.service';
import { DEFAULT_CONSECUTIVE_DAYS, DEFAULT_INDICATOR_NUMBER, MAX_NUMBER_OF_DAYS } from 'src/environments/environment';
@Component({
  selector: 'app-defects',
  templateUrl: './defects.component.html',
  styleUrls: ['./defects.component.scss'],
})
export class DefectsComponent implements OnInit {
  fileLoaded = false;
  listMapName: any[] = [];
  selectedMap: any;
  selectedSector: any;
  selectedSectorId = 0;
  infoMapId: any = '';
  infoSectorName: any;
  anomalyFilterId: number = 0;
  listSectorName: any[] = [];
  @ViewChild(ApexGraphComponent) apexGraphComponent!: ApexGraphComponent;
  @ViewChild(MapComponent) mapComponent!: MapComponent;
  @ViewChild(MeasurementVariablesComponent)
  measurementVariablesComponent!: MeasurementVariablesComponent;
  thresholdForm: FormGroup | undefined;
  anomalyFilterRequest!: any;
  parametros: any = {};
  archivo: File | null = null;
  valor14 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
  mapName: string = '';

  constructor(
    private matDialog: MatDialog,
    private fileUploadService: FileUploadService,
    private sectorService: SectorService,
    private mapService: MapService,
    private anomalyFilterService: AnomalyFilterService,
    private fb: FormBuilder,
    private anomalyService: AnomalyService,
    private loaderService: LoaderService,
    private authService: AuthenticationService
  ) {}

  public anomalyFilterForm: FormGroup = this.fb.group({
    number_of_days: [MAX_NUMBER_OF_DAYS, [Validators.required]],
    consecutive_days: [DEFAULT_CONSECUTIVE_DAYS, [Validators.required]],
    indicator_number: [DEFAULT_INDICATOR_NUMBER, [Validators.required]],
    tolerance: [ToleranceFilter.medium, [Validators.required]],
    sector: [null, [Validators.required]],
    mapa: [null, [Validators.required]],
  });

  ngOnInit() {
    this.initValues();
    this.mapList();
      }

  /**
   * Init value function
   * USER_EXPLOITATION The value depends on the user's authorization.
   * FIRST_DATA Constant related to the first data in the map list. The map list depends on the assigned explotaitation
  */
  initValues() {
    const USER_EXPLOITATION = localStorage.getItem('exploitation');
    const FIRST_DATA = 0
    this.mapService.getListMap().subscribe(
      data => {
        if (USER_EXPLOITATION != null) {
          let result = (this.listMapName = data.filter((item: any) => {
            return item.exploitation === parseInt(USER_EXPLOITATION, 10);
          }));
          this.infoMapId = result[FIRST_DATA].id.toString();
        }
      },
      error => {
        console.log('Error with the list map names', error);
      }
    );

  }

  /**
   * Actions related with the changes of the map
   * @param selectedMap Selected map on the list of maps for the exploitation
   */
  onMapSelected(selectedMap: any): void {
    if(this.selectedMap)this.fileLoaded = false;
    const sectorControl = this.anomalyFilterForm.get('sector');
    if (sectorControl) {
      sectorControl.reset();
    }
    this.infoMapId = selectedMap;
    this.selectedMap = selectedMap
    this.mapComponent.clearPreviousLayers();
    this.mapComponent.loadGeoJson(selectedMap);
    this.sectorList(selectedMap);
    this.thresholdForm = this.measurementVariablesComponent.thresholdForm;
    this.anomalyFilterRequest = {
      anomaly_filter_full: this.thresholdForm.value,
      anomaly_filter: this.anomalyFilterForm.value,
    };

    this.mapService.getDetailMap(this.infoMapId).subscribe(
      data => {
        this.mapName = data.name;
      },
      error => {
        console.error(error);
      }
    );
  }


  onIndicatorChange(e: any) {
    console.log('e', e);
  }

  /**
   * Gets the list of sectors associated with a map ID
   * @param mapId The map id for get the list of sectors
   */
  sectorList(mapId: string) {
    this.sectorService.getSector(parseInt(mapId)).subscribe(
      data => {
        this.listSectorName = data;
      },
      error => {
        console.log('Error with the list sector names', error);
      }
    );
  }

  /**
   * Saved of the thershold values
   * @param thresholdForm Thershold form
   */
  onEventData(thresholdForm: FormGroup): void {
    this.thresholdForm = thresholdForm;
    console.log("thi is voy biennnnnnnnn ----->> ", this.thresholdForm.value)
    if (this.anomalyFilterForm.valid && this.anomalyFilterForm.valid) {
      console.log("this is the anomaly filter form ----->> ", this.anomalyFilterForm.value)
      const anomalyFilterRequestToSave = {
        anomaly_filter: this.anomalyFilterForm.value,
        anomaly_filter_full: this.thresholdForm.value,
      };
      if (
        typeof anomalyFilterRequestToSave.anomaly_filter.sector !== 'number'
      ) {
        anomalyFilterRequestToSave.anomaly_filter.sector =
          this.anomalyFilterForm.value.sector.id;
      }

      console.log('first', anomalyFilterRequestToSave);
      this.anomalyFilterService.saveVariables(anomalyFilterRequestToSave)
        .subscribe();
    } else if (!this.anomalyFilterForm.valid)
      Swal.fire(
        '¡Almacenamiento fallido!',
        'Las variables difieren según el sector. Para guardar cambios debe seleccionar mapa y sector ',
        'error'
      );
    else if (!this.anomalyFilterForm.valid)
      Swal.fire('¡Almacenamiento fallido!', 'Complete el formulario', 'error');
  }

  /**
   * Actions related with the change of sector
   * @param selectedSector Sector selected
   */
  onSectorSelected(selectedSector: any): void {
    if(this.selectedSector)this.fileLoaded = false;
    this.selectedSector = selectedSector;
    this.selectedSectorId = selectedSector.id;
    this.infoSectorName = selectedSector.name;

    this.anomalyFilterService
      .findAnomalyFilterBySectorAndTolerance(this.selectedSectorId, ToleranceFilter.medium)
      .subscribe(data => {
        data[0].sector = this.selectedSector;
        this.anomalyFilterForm.patchValue(data[0]);
      });
    this.anomalyFilterService
      .getIndicatorThresholdBySectorIdAndTolerance(
        this.selectedSectorId,
        ToleranceFilter.medium
      )
      .subscribe(data => {
        this.thresholdForm!.setValue(data);
      });

  }

  /**
   * Actions related with the change of tolerance
   */
  onToleranceChange($event: any) {
    const tolerance = $event;
    this.anomalyFilterService
      .findAnomalyFilterBySectorAndTolerance(this.selectedSectorId, tolerance)
      .subscribe(data => {
        data[0].sector = this.selectedSector;
        this.anomalyFilterForm.patchValue(data[0]);
      });
    this.anomalyFilterService
      .getIndicatorThresholdBySectorIdAndTolerance(
        this.selectedSectorId,
        tolerance
      )
      .subscribe(data => {
        // this.thresholdForm!.reset();
        this.thresholdForm!.setValue(data);
      });
  }

  /**
   * Function for the search of defects o leaks by sector
   * @returns Metrics to display in the graphs and the map according to the information provided in the filters and thresholds
   * Or returns error messages according to system validations
   */
  buttonAnomaly() {
    // this.apexGraphComponent.ngOnInit();
    this.anomalyFilterForm.get('sector')?.markAsTouched();
    if (this.anomalyFilterForm.valid) {
      this.mapComponent.clearPreviousLayers();
      this.parametros = this.thresholdForm?.value;
      const numberOfDaysControl = this.anomalyFilterForm?.get('number_of_days');
      const numberOfIndicatorsControl = this.anomalyFilterForm?.get('indicator_number');
      const consecutiveDays = this.anomalyFilterForm.value.consecutive_days;

      if (numberOfDaysControl && numberOfIndicatorsControl) {
        const valorNumberOfDays = numberOfDaysControl.value;
        const valorNumberOfIndicators = numberOfIndicatorsControl.value;

        if (!this.archivo) {
          console.error('Debe seleccionar un archivo.');
          return;
        }
        if (this.archivo) {
          this.loaderService.showLoader();
          this.anomalyService
            .getAnomalySector(
              this.mapName,
              valorNumberOfDays,
              valorNumberOfIndicators,
              this.archivo,
              this.parametros
            )
            .subscribe(
              data => {
                this.mapComponent.searchAnomaly(
                  this.infoMapId,
                  this.infoSectorName,
                  consecutiveDays,
                  data
                );
                console.log("data", data)
                console.log("this.parametros", this.parametros)
                this.apexGraphComponent.clearAnotations();
                this.apexGraphComponent.loadGraph(data, this.parametros);
                this.loaderService.hideLoader();
              },
              error => {
                this.loaderService.hideLoader();
                const errorMessage = error.error.Error;
                if (error.status === 400) {
                  Swal.fire(
                    'Error',
                    'El fichero no tiene la estructura esperada. Por favor, descargue de nuevo el fichero de la fuente e inténtelo de nuevo',
                    'error'
                  );
                } else if (error.status === 415) {
                  const errorMessage = error.error.Error;
                  Swal.fire(
                    'Error',
                    'Los archivos de entrada no tienen el formato correcto.<br><br>El fichero debe de ser formato Excel',
                    'error'
                  );
                } else if (error.status === 401) {
                  Swal.fire(
                    'Error',
                    'Error en la autenticación del usuario',
                    'error'
                  );
                } else if (error.status === 404) {
                  Swal.fire('Error', 'No se encuentra', 'error');
                } else {
                  Swal.fire(
                    'Error',
                    'Hubo un problema al cargar los archivos.<br><br>Revise que su explotación sea apta para recibir datos metereológicos. En caso de que no ser asi, desmarque la casilla, guarde el filtro y envíe de nuevo ',
                    'error'
                  );
                }
                console.error(error);
              }
            );
        }
      }
    } else {
      Swal.fire(
        '¡Búsqueda fallida!',
        'No se completo la información de los filtros',
        'error'
      );
    }
  }

  /**
   * Gets the map list
   */
  mapList() {
    const exploitation = localStorage.getItem('exploitation');
    this.mapService.getListMap().subscribe(
      data => {
        if (exploitation != null) {
          let result = (this.listMapName = data.filter((item: any) => {
            return item.exploitation === parseInt(exploitation, 10);
          }));
        }
      },
      error => {
        console.log('Error with the list map names', error);
      }
    );
  }

  get toleranceFilter(): ToleranceFilter[] {
    return this.anomalyFilterService.tolerances;
  }
  get indicator_number(): number[] {
    return this.anomalyFilterService.indicator_number;
  }
  get number_of_days(): number[] {
    return this.anomalyFilterService.number_of_days;
  }

  /**
   * Function to upload files
   */
  onClick() {
    const dialogRef = this.matDialog.open(FileUploadComponent, {
      width: '800px',
      height: '400px',
      data: {
        title: 'Cargar fichero de anomalías',
        description: 'Datos de la explotación *',
        allowedExtensions: ['.xlsx'],
        minFiles: 1,
        maxFiles: 1,
      },
    });
    dialogRef.componentInstance.filesLoaded.subscribe((file: File) => {
      this.archivo = file;
    });

    dialogRef.afterClosed().subscribe(result => {
      this.fileLoaded = result === 'success';
    });
  }
  onInfo() {
    const dialogRef = this.matDialog.open(InfoCardComponent, {
      width: '80%',
      height: '40.25%',
      data: {
        variable: 0,
      },
    });
  }
}
