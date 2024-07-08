import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator, MatPaginatorIntl } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { FileUploadComponent } from 'src/app/components/file.upload/file.upload.component';
import { FileUploadService } from 'src/app/core/services/file-upload.service';
import { HydraulicPerformanceService } from 'src/app/core/services/hydraulic-performance.service';
import { MapService } from 'src/app/core/services/map.service';
import { SectorService } from 'src/app/core/services/sector.service';
import Swal from 'sweetalert2';
import {
  HPExpectedVariables,
  HydraulicPerformanceResponse,
} from '../../../core/models/interfaces/hydraulic-performance-response';
import { ApexGraphHpComponent } from './apex-graph-hp/apex-graph-hp.component';
import {
  catchError,
  filter,
  finalize,
  map,
  never,
  of,
  switchMap,
  tap,
  throwError,
} from 'rxjs';
import { LoaderService } from 'src/app/core/services/loader.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-hydraulicc-performance',
  templateUrl: './hydraulicc-performance.component.html',
  styleUrls: ['./hydraulicc-performance.component.scss'],
})
export class HydrauliccPerformanceComponent implements AfterViewInit {
  listMapName: any[] = [];
  listSectorName: any[] = [];
  displayedColumns: string[] = [
    'N°',
    'bimester',
    'hp_total_percentage',
    'eliminar',
  ];
  dataSource = new MatTableDataSource<HydraulicPerformanceResponse>(
    ELEMENT_DATA
  );
  selectedMap: any;
  selectedSector: any;
  fileAccept = false;
  files: File[] = [];
  city: string = '';
  blurred = false;
  hystoricList: any[] = [];
  newRegister = false;
  newData: any = {};
  listBimester: any[] = [1, 2, 3, 4, 5, 6];

  public performanceForm: FormGroup = this.formBuilder.group({
    map: [null, Validators.required],
    sector: [null, Validators.required],
    bimester: [null, Validators.required],
    year: [null, Validators.required],
  });

  @ViewChild(MatPaginator) paginatorHP!: MatPaginator;
  @ViewChild(ApexGraphHpComponent) apexGraphHPComponent!: ApexGraphHpComponent;

  constructor(
    private mapService: MapService,
    private matDialog: MatDialog,
    private fileUploadService: FileUploadService,
    private sectorService: SectorService,
    private paginator: MatPaginatorIntl,
    private hydraulicService: HydraulicPerformanceService,
    private loaderService: LoaderService,
    private formBuilder: FormBuilder
  ) {
    this.paginator.itemsPerPageLabel = 'Registros por página';
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginatorHP;
    this.mapList();
  }

  /**
   * List of maps of the current user's exploitation
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

  /**
   * Assignment values according to the selected map
   * @param selectedMap Map selected
   */
  onMapSelected(selectedMap: any): void {
    this.city = selectedMap.name;
    this.sectorList(selectedMap.id);
    this.selectedMap = selectedMap;
  }

  /**
   * Sector list of the selected map
   * @param mapId Id of the map selected
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
   * Actions after selecting the sector
   * @param selectedSector Sector selected
   */
  onSectorSelected(selectedSector: any): void {
    this.selectedSector = selectedSector;
    this.listData();
  }

  /**
   * Function to open the file upload window
   */
  onClick() {
    const dialogRef = this.matDialog.open(FileUploadComponent, {
      width: '800px',
      height: '400px',
      data: {
        title: 'Cargar ficheros',
        description:
          'Datos de consumo *, Datos de agua suministrada de la explotación* y datos de origen de lecturas (opcional). Recuerde: Los ficheros obligatorios deben llamarse asi: Suministrado.xlsx y Registrado.xlsx ó Registrado.csv',
        allowedExtensions: ['.xlsx', '.csv'],
        minFiles: 2,
        maxFiles: 3,
        validateName: true,
        optional: true,
        requiredNames: ['Registrado', 'Suministrado'],
      },
    });

    dialogRef.componentInstance.filesLoaded.subscribe((file: File) => {
      if (file.name.includes('Suministrado')) {
        this.files[0] = file;
      } else if (file.name.includes('Registrado')) {
        this.files[1] = file;
      } else {
        this.files[2] = file;
      }

      if (this.files.length === 3) {
        this.fileAccept = true;
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (this.selectedMap && this.selectedSector)
        this.fileAccept = result === 'success';
    });
  }

  /**
   * Function for delete registers
   * @param id Id del registro a eliminar
   */
  deleteData(id: number) {
    this.hydraulicService.deleteHydraulicPerformanceById(id).subscribe(data => {
      this.listData();
      Swal.fire('Eliminado', 'Se ha eliminado correctamente', 'success');
    });
  }

  /**
   * This fuction send to the cetaqua backend: the header with the city and max 3 files.
   */
  sendDataCq() {
    if (this.performanceForm.valid) {
      const mapControl = this.performanceForm.get('map');
      const sectorControl = this.performanceForm.get('sector');
      const bimesterControl = this.performanceForm.get('bimester');
      const yearControl = this.performanceForm.get('year');
      if (bimesterControl && yearControl && mapControl && sectorControl) {
        const map = mapControl.value;
        const sector = sectorControl.value;
        const bimester = bimesterControl.value;
        const year = yearControl.value;

        this.hydraulicService
          .findHydraulicPerformanceBySectorIdAndYearAndBimester(
            sector.id,
            year,
            bimester
          )
          .subscribe((res: HydraulicPerformanceResponse) => {
            if (res.bimester == bimester && res.year == year) {
              Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Ya existe un registro para este año y bimestre, si desea guardarlo primero elimínelo manualmente y vuelva a intentarlo.',
                footer: 'Falla de integridad de datos',
              });
              return;
            }
            else {
              this.loaderService.showLoader();
              this.hydraulicService
                .sendData(this.files, map.name, sector.name, year, bimester)
                .subscribe(
                  data => {
                    this.newData = data;
                    const hp_variables = {
                      contract_number: this.newData.Num_contratos,
                      liters_supplied: this.newData.Litros_Suministrados,
                      percentage_adjustment: this.newData.Porcentaje_Ajuste,
                      percentage_telereading: this.newData.Porcentaje_Telelectura,
                    };
                    const hp_expected_variables = {
                      hp_expected: this.newData.RH_esperado,
                      supplied_expected: this.newData.Suministrado_esperado,
                      registed_expected: this.newData.Registrado_esperado,
                    };
                    const requestData = {
                      year: year,
                      bimester: bimester,
                      sector: sector.id,
                      hp_total_percentage: this.newData.Porcentaje_RH_total,
                      hp_variables: hp_variables,
                      hp_expected_variables: hp_expected_variables,
                    };
                    this.newData.sector_id = sector.id;
                    this.loaderService.hideLoader();
                    this.hydraulicService
                      .findHydraulicPerformanceBySectorIdAndYearAndBimester(
                        sector.id,
                        year,
                        bimester
                      )
                      .subscribe(data => {
                        const dataRes = data;
                        if (dataRes.length === 0) {
                          this.hydraulicService
                            .addHydraulicPerformanceBySector(requestData)
                            .subscribe(data => {
                              this.listData();
                            });
                          Swal.fire('Registro guardado correctamente', '', 'success');
                        } else {
                          this.listData();
                          Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: 'Ya existe un registro para este año y bimestre, si desea guardarlo primero elimínelo manualmente y vuelva a intentarlo.',
                            footer: 'Falla de integridad de datos',
                          });
                        }
                      });
                  },
                  error => {
                    this.loaderService.hideLoader();
                    if (error.status === 422) {
                      Swal.fire(
                        'Error',
                        'Los archivos de entrada no tienen los datos/columnas requeridas.',
                        'error'
                      );
                    } else if (error.status === 415) {
                      Swal.fire(
                        'Error',
                        'Los archivos de entrada no tienen el formato correcto.',
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
                    } else if (error.status === 400) {
                      Swal.fire('Algo salió mal', 'Petición fallida.', 'error');
                    } else {
                      Swal.fire(
                        'Error',
                        'Hubo un problema al cargar los archivos',
                        'error'
                      );
                      console.error('Error en la carga de archivos:', error);
                    }
                    console.error(error);
                  }
                );
            }
          });



        this.blurred = true;
        this.newRegister = true;
        this.loadDataSource();
        this.fileAccept = false;
        this.hystoricList = [];
      }
    }
  }

  /**
   * Allows visibility of the graph and table only if map and sector have been selected
   */
  listData() {
    this.newRegister = false;
    if (this.selectedMap && this.selectedSector) {
      this.blurred = true;
      this.loadDataSource();
    } else
      Swal.fire(
        'Recuerde',
        'Debe diligenciar el mapa y el sector para realizar su búsqueda',
        'warning'
      );
  }

  /**
   * Gives a historical list of the hydraulic performance
   */
  public loadDataSource() {
    this.hydraulicService
      .findHydraulicPerformanceBySector(this.selectedSector.id)
      .subscribe(data => {
        if (data[0].length === 0 && this.newRegister == false) {
          Swal.fire({
            title: 'Sin datos',
            text: 'No hay datos para mostrar',
            icon: 'question',
          });
          this.dataSource =
            new MatTableDataSource<HydraulicPerformanceResponse>([]);
          return;
        }
        this.hystoricList = data[0];
        if (this.newRegister) this.newDataPerfonamce(this.newData);
        this.dataSource = new MatTableDataSource<HydraulicPerformanceResponse>(
          this.hystoricList.reverse()
        );
        this.dataSource.paginator = this.paginatorHP;
      });
    this.apexGraphHPComponent.loadGraph(this.selectedSector.id);
  }

  /**
   * Function to insert the new data
   * @param data response in the assignment correction module
   */
  public newDataPerfonamce(data: any) {
    let newData = {
      sector: data.Sector,
      year: data.Año,
      bimester: data.Bimestre,
      hp_total_percentage: data.Porcentaje_RH_total,
      hp_variables: {
        contract_number: data.Num_contratos,
        liters_supplied: data.Litros_Suministrados,
        percentage_adjustment: data.Porcentaje_Ajuste,
        percentage_telereading: data.Porcentaje_Telelectura,
      },
      hp_expected_variables: {
        hp_expected: data.RH_esperado,
        supplied_expected: data.Suministrado_esperado,
        registed_expected: data.Registrado_esperado,
      },
    };
    this.hystoricList.unshift(newData);
    this.dataSource.data = this.hystoricList;
  }
}

let ELEMENT_DATA: HydraulicPerformanceResponse[] = [
  { id: 1, sector: 1, year: 2019, bimester: 1, hp_total_percentage: 0 },
  { id: 2, sector: 1, year: 2019, bimester: 2, hp_total_percentage: 0 },
  { id: 3, sector: 1, year: 2019, bimester: 3, hp_total_percentage: 0 },
  { id: 4, sector: 1, year: 2019, bimester: 4, hp_total_percentage: 0 },
  { id: 5, sector: 1, year: 2020, bimester: 1, hp_total_percentage: 0 },
  { id: 6, sector: 1, year: 2020, bimester: 2, hp_total_percentage: 0 },
  { id: 7, sector: 1, year: 2020, bimester: 3, hp_total_percentage: 0 },
  { id: 8, sector: 1, year: 2020, bimester: 4, hp_total_percentage: 0 },
  { id: 9, sector: 1, year: 2021, bimester: 1, hp_total_percentage: 0 },
  { id: 10, sector: 1, year: 2021, bimester: 2, hp_total_percentage: 0 },
  { id: 11, sector: 1, year: 2021, bimester: 3, hp_total_percentage: 0 },
  { id: 12, sector: 1, year: 2021, bimester: 4, hp_total_percentage: 0 },
];
