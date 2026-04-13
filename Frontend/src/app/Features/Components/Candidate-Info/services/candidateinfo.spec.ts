import { TestBed } from '@angular/core/testing';

import { Candidateinfo } from './candidateinfoSer';

describe('Candidateinfo', () => {
  let service: Candidateinfo;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Candidateinfo);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
