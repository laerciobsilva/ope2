import { TestBed } from '@angular/core/testing';
import { CategoriaService } from './categoria.service';

describe('CategoriaItemCardapioService', () => {
  let service: CategoriaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CategoriaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
