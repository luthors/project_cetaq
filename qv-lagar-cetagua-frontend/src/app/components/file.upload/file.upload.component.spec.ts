import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { FileUploadComponent } from './file.upload.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { NgxFileDropModule } from 'ngx-file-drop';
import { MatIconModule } from '@angular/material/icon';

describe('FileUploadComponent', () => {
  let component: FileUploadComponent;
  let fixture: ComponentFixture<FileUploadComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FileUploadComponent],
      imports:[HttpClientTestingModule, MatDialogModule, NgxFileDropModule, MatIconModule],
      providers: [
        { provide: MatDialogRef, useValue: {} },
        { provide: MAT_DIALOG_DATA, useValue: {} }
      ]
    });
    fixture = TestBed.createComponent(FileUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
