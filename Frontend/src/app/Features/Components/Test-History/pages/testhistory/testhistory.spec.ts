import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Testhistory } from './testhistory';

describe('Testhistory', () => {
  let component: Testhistory;
  let fixture: ComponentFixture<Testhistory>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Testhistory]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Testhistory);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
