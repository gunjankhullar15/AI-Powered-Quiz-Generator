import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Createtest } from './createtest';

describe('Createtest', () => {
  let component: Createtest;
  let fixture: ComponentFixture<Createtest>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Createtest]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Createtest);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
