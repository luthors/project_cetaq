import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { LoaderModalComponent } from '../../components/loader-modal/loader-modal.component';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {
  constructor(private dialog: MatDialog) { }
  showLoader(): void {
    this.dialog.open(LoaderModalComponent, {
      disableClose: true,
      panelClass: 'loader-modal',
    });
  }
  hideLoader(): void {
    this.dialog.closeAll();
  }
}
