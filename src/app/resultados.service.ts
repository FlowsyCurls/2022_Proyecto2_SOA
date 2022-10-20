import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ResultadosService {

  constructor(private http: HttpClient) { }
  // Metodo que se comunica con el backend para obetener la informacion de la base de datos
  getResultados() {
    return this.http.get<Array<any>>('http://localhost:8090');
  }

}
