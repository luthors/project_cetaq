import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoaderModalComponent } from './loader-modal.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

describe('LoaderModalComponent', () => {
  let component: LoaderModalComponent;
  let fixture: ComponentFixture<LoaderModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [LoaderModalComponent],
      imports: [MatProgressSpinnerModule]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoaderModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should display a spinner', () => {
    const spinnerElement: HTMLElement = fixture.nativeElement.querySelector('mat-spinner');
    expect(spinnerElement).toBeTruthy();
  });
});
