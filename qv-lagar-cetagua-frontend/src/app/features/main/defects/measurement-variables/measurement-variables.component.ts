import {
  Component,
  EventEmitter,
  OnInit,
  Output,
  ViewChild,
} from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import {
  AnomalyFilterRequest,
  Flow,
  ToleranceFilter,
} from 'src/app/core/models/interfaces/anomaly-filter';
import { MatDialog } from '@angular/material/dialog'; // {MatDialog}
import { IndicatorThresholdService } from 'src/app/core/services/indicator-threshold.service';
import { DefectsComponent } from '../defects.component';
import { InfoCardComponent } from 'src/app/components/info.card/info.card.component';
import { DailyVolume } from '../../../../core/models/interfaces/anomaly-filter';
import { HelpInformationService } from '../../../../core/services/help-information.service';
import Swal from 'sweetalert2';
@Component({
  selector: 'app-measurement-variables',
  templateUrl: './measurement-variables.component.html',
  styleUrls: ['./measurement-variables.component.scss'],
})
export class MeasurementVariablesComponent implements OnInit {
  @Output() eventData = new EventEmitter<FormGroup>();
  @ViewChild(DefectsComponent) defectsComponent!: DefectsComponent;
  editThreshold = new FormControl(false);
  anomalyFilterRequest!: AnomalyFilterRequest;
  anomalyFilterForm!: FormGroup;
  showCard = false;
  info: any;

  public thresholdForm: FormGroup = this.fb.group({
    flow: this.fb.group({
      active: [true],
      meanWeekDays: [7, [Validators.required, Validators.min(0)]],
      // meanSurrounding: [0, [Validators.required, Validators.min(0)]],
      hours: [2, [Validators.required, Validators.min(0)]],
      tolerance: [
        0.2,
        [Validators.required, Validators.min(0), Validators.max(1)],
      ],
    }),
    minFlow: this.fb.group({
      active: [true],
      movingAverageDays: [
        7,
        [Validators.required, Validators.min(4), Validators.max(14)],
      ],
      fixedAverageDays: [
        60,
        [Validators.required, Validators.min(30), Validators.max(150)],
      ],
      weightAverage: [
        1,
        [Validators.required, Validators.min(0.5), Validators.max(2.5)],
      ],
      weightDeviation: [
        1.2,
        [Validators.required, Validators.min(0.5), Validators.max(2.0)],
      ],
      tolerance: [
        0.2,
        [Validators.required, Validators.min(0), Validators.max(1)],
      ],
    }),
    dailyVolume: this.fb.group({
      active: [true],
      movingAverageDays: [
        7,
        [Validators.required, Validators.min(4), Validators.max(14)],
      ],
      fixedAverageDays: [
        60,
        [Validators.required, Validators.min(30), Validators.max(150)],
      ],
      weightAverage: [
        1,
        [Validators.required, Validators.min(0.5), Validators.max(2.5)],
      ],
      weightDeviation: [
        1.2,
        [Validators.required, Validators.min(0.5), Validators.max(2.0)],
      ],
      tolerance: [
        0.2,
        [Validators.required, Validators.min(0), Validators.max(1)],
      ],
    }),
    pressure: this.fb.group({
      active: [true],
      movingAverageDays: [
        7,
        [Validators.required, Validators.min(4), Validators.max(14)],
      ],
      weightAverage: [
        1,
        [Validators.required, Validators.min(0.5), Validators.max(2.5)],
      ],
      weightDeviation: [
        1.2,
        [Validators.required, Validators.min(0.5), Validators.max(2.0)],
      ],
    }),
    minFlowMultmeanFlow: this.fb.group({
      active: [true],
      movingAverageDays: [
        7,
        [Validators.required, Validators.min(4), Validators.max(14)],
      ],
      weightAverage: [
        1,
        [Validators.required, Validators.min(0.5), Validators.max(2.5)],
      ],
      weightDeviation: [
        1.2,
        [Validators.required, Validators.min(0.5), Validators.max(2.0)],
      ],
    }),
    minFlowDivmeanFlow: this.fb.group({
      active: [true],
      movingAverageDays: [
        7,
        [Validators.required, Validators.min(4), Validators.max(14)],
      ],
      weightAverage: [
        1,
        [Validators.required, Validators.min(0.5), Validators.max(2.5)],
      ],
      weightDeviation: [
        1.2,
        [Validators.required, Validators.min(0.5), Validators.max(2.0)],
      ],
    }),
    meteo: this.fb.group({
      active: [true],
    }),
  });

  constructor(
    private matDialog: MatDialog,
    private fb: FormBuilder,
    private thresholdService: IndicatorThresholdService,
    private helpInformationServive: HelpInformationService
  ) {}
  onSubmitAnomalyForm(e: any): void {
    if (this.thresholdForm.valid) {
      Swal.fire('Guardado','Se ha guardado la configuracion de variables correctamante', 'success');
      this.eventData.emit(this.thresholdForm);
    } else {
      Swal.fire('Error', 'Hay campos vacíos o incorrectos', 'error');
    }
  }
  onClick(variable: number, index: number) {
    const dialogRef = this.matDialog.open(InfoCardComponent, {
      width: '80%',
      height: '90%',
      data: {
        variable: variable,
        index: index
      },
    });
  }

  onClick2(variable: number, index: number) {
    const dialogRef = this.matDialog.open(InfoCardComponent, {
      width: '80%',
      height: 'auto',
      data: {
        variable: variable,
        index: index
      },
    });
  }

  ngOnInit() {
    this.thresholdService.getIndicatorsList().subscribe(
      data => {
        const initData = data[0].id
        this.thresholdService.getThresholdList(initData).subscribe(
          defaultValues => {
            this.thresholdForm.patchValue(defaultValues);
          },
          error => {
            console.log('Error with the default values');
          }
        );
      },
      error => {
        console.log('Error with the default values');
      }
    );



    this.helpInformationServive.getHelpInformation()
      .subscribe({
        next: (info: any) => {
          this.info = info;
        },
        error: (error: any) => {
          console.error(error);
        },
        complete: () => {
        }
      })
  }

}
