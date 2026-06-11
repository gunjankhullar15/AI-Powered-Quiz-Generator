import { TestBed } from '@angular/core/testing';

import { Createtest } from './createtestSer';

describe('Createtest', () => {
  let service: Createtest;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Createtest);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
