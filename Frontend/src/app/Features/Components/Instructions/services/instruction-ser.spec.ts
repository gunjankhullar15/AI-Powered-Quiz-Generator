import { TestBed } from '@angular/core/testing';

import { InstructionSer } from './instruction-ser';

describe('InstructionSer', () => {
  let service: InstructionSer;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InstructionSer);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
