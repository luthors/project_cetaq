import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HelpInformationService } from 'src/app/core/services/help-information.service';

@Component({
  selector: 'app-info.card',
  templateUrl: './info.card.component.html',
  styleUrls: ['./info.card.component.scss']
})



export class InfoCardComponent implements OnInit {
    info: any;
    vari: any;
  constructor(
    public dialogRef: MatDialogRef<InfoCardComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private helpInformationServive: HelpInformationService) { }
  ngOnInit(): void {
    this.helpInformationServive.getHelpInformation()
      .subscribe({
        next: (info: any) => {
          this.info = info;
          console.log(info);
        },
        error: (error: any) => {
          console.error(error);
        },
        complete: () => {
          console.log('completado')
        }
      })
      this.helpInformationServive.getHelpInfoVariables()
      .subscribe({
        next: (vari: any) => {
          this.vari = vari;
          console.log(vari);
        },
        error: (error: any) => {
          console.error(error);
        },
        complete: () => {
          console.log('completado vari')
        }
      })
  }
}

