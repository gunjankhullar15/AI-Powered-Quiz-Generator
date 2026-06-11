import { TestBed } from '@angular/core/testing';

import { ResultSer } from './result-ser';

describe('ResultSer', () => {
  let service: ResultSer;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ResultSer);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
