import { TestBed } from '@angular/core/testing';

import { TestPage1Ser } from './test-page1-ser';

describe('TestPage1Ser', () => {
  let service: TestPage1Ser;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TestPage1Ser);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
