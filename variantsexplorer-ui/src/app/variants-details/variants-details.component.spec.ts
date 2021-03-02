import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VariantsDetailsComponent } from './variants-details.component';

describe('VariantDetailsComponent', () => {
  let component: VariantsDetailsComponent;
  let fixture: ComponentFixture<VariantsDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VariantsDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VariantsDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
