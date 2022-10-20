import { Component, OnInit } from '@angular/core';
import * as os from 'os';
import { ResultadosService } from '../resultados.service'
import { first } from 'rxjs';
@Component({
  selector: 'app-resultados',
  templateUrl: './resultados.component.html',
  styleUrls: ['./resultados.component.css']
})
export class ResultadosComponent implements OnInit {

  resultados: Array<any> = []

  constructor(private resultadosSrv: ResultadosService) { }

  ngOnInit(): void {
    // Se asiganan los datos obtenidos del get resultados a la variable resultados para mostrar 
    this.resultadosSrv.getResultados().pipe(first()).subscribe(response => { this.resultados = response; });

  }

}
