import { TestBed } from '@angular/core/testing';

import { TestSer } from './test-ser';

describe('TestSer', () => {
  let service: TestSer;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TestSer);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
