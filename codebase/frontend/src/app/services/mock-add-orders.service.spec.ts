import { TestBed } from '@angular/core/testing';

import { MockAddOrdersService } from './mock-add-orders.service';

describe('MockAddOrdersService', () => {
  let service: MockAddOrdersService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MockAddOrdersService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
