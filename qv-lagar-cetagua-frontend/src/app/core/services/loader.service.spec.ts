import { TestBed } from '@angular/core/testing';

import { LoaderService } from './loader.service';
import { MatDialog } from '@angular/material/dialog';
import { LoaderModalComponent } from 'src/app/components/loader-modal/loader-modal.component';

describe('LoaderService', () => {
  let service: LoaderService;
  let dialogSpy: jasmine.SpyObj<MatDialog>;

  beforeEach(() => {
    const spy = jasmine.createSpyObj('MatDialog', ['open', 'closeAll']);

    TestBed.configureTestingModule({
      providers: [
        LoaderService,
        { provide: MatDialog, useValue: spy }
      ]
    });
    service = TestBed.inject(LoaderService);
    dialogSpy = TestBed.inject(MatDialog) as jasmine.SpyObj<MatDialog>;
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should call open method of MatDialog when showLoader is called', () => {
    service.showLoader();
    expect(dialogSpy.open).toHaveBeenCalledWith(LoaderModalComponent, { disableClose: true, panelClass: 'loader-modal' });
  });

  it('should call closeAll method of MatDialog when hideLoader is called', () => {
    service.hideLoader();
    expect(dialogSpy.closeAll).toHaveBeenCalled();
  });
});
