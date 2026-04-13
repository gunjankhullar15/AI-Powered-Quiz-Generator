import { TestBed } from '@angular/core/testing';

import { Testhistory } from './testhistory';

describe('Testhistory', () => {
  let service: Testhistory;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Testhistory);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
