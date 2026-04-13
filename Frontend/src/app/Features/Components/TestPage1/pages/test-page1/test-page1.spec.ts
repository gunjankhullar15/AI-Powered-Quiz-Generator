import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestPage1 } from './test-page1';

describe('TestPage1', () => {
  let component: TestPage1;
  let fixture: ComponentFixture<TestPage1>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestPage1]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestPage1);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
