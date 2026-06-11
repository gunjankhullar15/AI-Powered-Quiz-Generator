import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Candidateinfo } from './candidateinfo';

describe('Candidateinfo', () => {
  let component: Candidateinfo;
  let fixture: ComponentFixture<Candidateinfo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Candidateinfo]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Candidateinfo);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
