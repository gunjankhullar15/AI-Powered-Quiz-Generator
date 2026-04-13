import { TestBed } from '@angular/core/testing';

import { NavSer } from './nav-ser';

describe('NavSer', () => {
  let service: NavSer;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NavSer);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
