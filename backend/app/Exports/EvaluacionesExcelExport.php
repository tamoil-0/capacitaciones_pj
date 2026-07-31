<?php

namespace App\Exports;

use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;
use PhpOffice\PhpSpreadsheet\Style\Alignment;
use PhpOffice\PhpSpreadsheet\Style\Border;
use PhpOffice\PhpSpreadsheet\Style\Fill;
use PhpOffice\PhpSpreadsheet\Style\Color;
use PhpOffice\PhpSpreadsheet\Worksheet\Drawing;
use PhpOffice\PhpSpreadsheet\Chart\Chart;
use PhpOffice\PhpSpreadsheet\Chart\DataSeries;
use PhpOffice\PhpSpreadsheet\Chart\DataSeriesValues;
use PhpOffice\PhpSpreadsheet\Chart\Legend;
use PhpOffice\PhpSpreadsheet\Chart\PlotArea;
use PhpOffice\PhpSpreadsheet\Chart\Title as ChartTitle;

class EvaluacionesExcelExport
{
    protected $evaluaciones;
    protected $evento;
    protected $tipoEvento;
    protected $spreadsheet;
    protected $sheet;
    protected $filaFinalDatos;
    protected $contadorAprobados;
    protected $contadorDesaprobados;

    public function __construct($evaluaciones, $evento = null, $tipoEvento = 'Todos')
    {
        $this->evaluaciones = $evaluaciones;
        $this->evento = $evento;
        $this->tipoEvento = $tipoEvento;
        $this->filaFinalDatos = 0;
        $this->contadorAprobados = 0;
        $this->contadorDesaprobados = 0;
    }

    public function export($rutaArchivo)
    {
        $this->spreadsheet = new Spreadsheet();
        $this->sheet = $this->spreadsheet->getActiveSheet();
        
        // Configurar hoja
        $this->sheet->setTitle('Evaluaciones');
        
        // Crear encabezado elegante
        $this->crearEncabezado();
        
        // Crear tabla de datos
        $this->crearTablaDatos();
        
        // Crear estadísticas
        $this->crearEstadisticas();
        
        // Ajustar anchos de columna
        $this->ajustarColumnas();
        
        // Guardar archivo
        $writer = new Xlsx($this->spreadsheet);
        $writer->save($rutaArchivo);
    }

    protected function crearEncabezado()
    {
        // ═══════════════════════════════════════════════════════════
        // 📋 ENCABEZADO PRINCIPAL - Filas 1-5
        // ═══════════════════════════════════════════════════════════
        
        // Fila 1: Título principal (merger A1:N2)
        $this->sheet->mergeCells('A1:N2');
        $this->sheet->setCellValue('A1', 'SISTEMA DE ASISTENCIA Y CALIFICACIÓN DE EXÁMENES - REPORTE DE EVALUACIONES');
        $this->sheet->getStyle('A1')->applyFromArray([
            'font' => [
                'bold' => true,
                'size' => 18,
                'color' => ['rgb' => 'FFFFFF'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
                'vertical' => Alignment::VERTICAL_CENTER,
            ],
            'fill' => [
                'fillType' => Fill::FILL_SOLID,
                'startColor' => ['rgb' => '1F4E78'], // Azul oscuro profesional
            ],
        ]);
        
        // Fila 3: Información del reporte
        $this->sheet->mergeCells('A3:N3');
        $eventoNombre = $this->evento ? $this->evento->nombre : 'Todos los eventos';
        $this->sheet->setCellValue('A3', "Evento: {$eventoNombre} | Tipo: {$this->tipoEvento}");
        $this->sheet->getStyle('A3')->applyFromArray([
            'font' => [
                'bold' => true,
                'size' => 12,
                'color' => ['rgb' => '1F4E78'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
            ],
            'fill' => [
                'fillType' => Fill::FILL_SOLID,
                'startColor' => ['rgb' => 'E7E6E6'], // Gris claro
            ],
        ]);
        
        // Fila 4: Fecha de generación
        $this->sheet->mergeCells('A4:N4');
        $this->sheet->setCellValue('A4', 'Generado: ' . now()->format('d/m/Y H:i:s'));
        $this->sheet->getStyle('A4')->applyFromArray([
            'font' => [
                'italic' => true,
                'size' => 10,
                'color' => ['rgb' => '595959'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
            ],
        ]);
        
        // Establecer altura de filas del encabezado
        $this->sheet->getRowDimension(1)->setRowHeight(30);
        $this->sheet->getRowDimension(3)->setRowHeight(25);
        $this->sheet->getRowDimension(4)->setRowHeight(20);
    }

    protected function crearTablaDatos()
    {
        // ═══════════════════════════════════════════════════════════
        // 📊 TABLA DE DATOS - Inicia en fila 6
        // ═══════════════════════════════════════════════════════════
        
        $filaInicio = 6;
        
        // Encabezados de la tabla
        $encabezados = [
            'A' => 'N°',
            'B' => 'DNI',
            'C' => 'APELLIDOS Y NOMBRES',
            'D' => 'TIPO EVENTO',
            'E' => 'EVENTO',
            'F' => 'FECHA EVALUACIÓN',
            'G' => 'TOTAL PREG.',
            'H' => 'CORRECTAS',
            'I' => 'INCORRECTAS',
            'J' => 'EN BLANCO',
            'K' => 'PUNTAJE',
            'L' => 'NOTA (%)',
            'M' => 'ESTADO',
            'N' => 'OBSERVACIONES',
        ];
        
        foreach ($encabezados as $col => $titulo) {
            $this->sheet->setCellValue("{$col}{$filaInicio}", $titulo);
        }
        
        // Estilo de encabezados de tabla
        $this->sheet->getStyle("A{$filaInicio}:N{$filaInicio}")->applyFromArray([
            'font' => [
                'bold' => true,
                'size' => 11,
                'color' => ['rgb' => 'FFFFFF'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
                'vertical' => Alignment::VERTICAL_CENTER,
            ],
            'fill' => [
                'fillType' => Fill::FILL_SOLID,
                'startColor' => ['rgb' => '4472C4'], // Azul
            ],
            'borders' => [
                'allBorders' => [
                    'borderStyle' => Border::BORDER_THIN,
                    'color' => ['rgb' => '000000'],
                ],
            ],
        ]);
        
        $this->sheet->getRowDimension($filaInicio)->setRowHeight(25);
        
        // ═══════════════════════════════════════════════════════════
        // 📝 DATOS DE LAS EVALUACIONES
        // ═══════════════════════════════════════════════════════════
        
        $fila = $filaInicio + 1;
        $contadorAprobados = 0;
        $contadorDesaprobados = 0;
        
        foreach ($this->evaluaciones as $index => $evaluacion) {
            $inscripcion = $evaluacion->inscripcionRel;
            $persona = $inscripcion ? $inscripcion->personaRel : null;
            $resultado = $evaluacion->resultadoRel;
            $eventoData = $inscripcion ? $inscripcion->eventoRel : null;
            
            if (!$persona || !$eventoData) {
                continue;
            }
            
            // ═══════════════════════════════════════════════════════════
            // 🔢 CÁLCULO DE ESTADÍSTICAS
            // ═══════════════════════════════════════════════════════════
            $totalPreguntas = $resultado->total_preguntas ?? 30;
            $puntaje = $resultado->puntaje ?? 0;
            
            // Contar respuestas marcadas en respuestas_omr
            $totalRespuestas = $evaluacion->respuestasOmr->count();
            
            // En blanco = preguntas que no fueron respondidas
            $enBlanco = $totalPreguntas - $totalRespuestas;
            
            // Si el puntaje es <= total_preguntas, asumimos que es número de correctas
            // Si es mayor, es un puntaje ponderado
            if ($puntaje <= $totalPreguntas) {
                // Caso 1: Puntaje = número de correctas directamente
                $correctas = (int) $puntaje;
                $incorrectas = $totalRespuestas - $correctas;
                $porcentaje = $totalPreguntas > 0 ? ($correctas / $totalPreguntas) * 100 : 0;
            } else {
                // Caso 2: Puntaje ponderado - No podemos deducir correctas/incorrectas exactas
                // Mostramos el puntaje como está y calculamos porcentaje basado en puntaje máximo
                $correctas = '-'; // No determinable
                $incorrectas = '-'; // No determinable
                $porcentaje = $totalPreguntas > 0 ? ($puntaje / ($totalPreguntas * 2)) * 100 : 0; // Asumiendo 2 puntos por pregunta
            }
            
            $aprobado = $resultado->aprobado ?? false;
            
            if ($aprobado) {
                $contadorAprobados++;
            } else {
                $contadorDesaprobados++;
            }
            
            // Datos de la fila
            $this->sheet->setCellValue("A{$fila}", $index + 1);
            $this->sheet->setCellValue("B{$fila}", $persona->dni);
            $this->sheet->setCellValue("C{$fila}", trim($persona->nombres . ' ' . $persona->apPaterno . ' ' . $persona->apMaterno));
            $this->sheet->setCellValue("D{$fila}", $eventoData->tipoEvento->nombre ?? 'N/A');
            $this->sheet->setCellValue("E{$fila}", $eventoData->nombre);
            $this->sheet->setCellValue("F{$fila}", $evaluacion->fecha_evaluacion->format('d/m/Y H:i'));
            $this->sheet->setCellValue("G{$fila}", $totalPreguntas);
            $this->sheet->setCellValue("H{$fila}", $correctas);
            $this->sheet->setCellValue("I{$fila}", $incorrectas);
            $this->sheet->setCellValue("J{$fila}", $enBlanco);
            $this->sheet->setCellValue("K{$fila}", $puntaje);
            $this->sheet->setCellValue("L{$fila}", $porcentaje);
            $this->sheet->setCellValue("M{$fila}", $aprobado ? 'APROBADO' : 'DESAPROBADO');
            $this->sheet->setCellValue("N{$fila}", $evaluacion->observaciones ?? '-');
            
            // Estilo de datos - Filas alternadas
            $colorFila = ($fila % 2 == 0) ? 'F2F2F2' : 'FFFFFF';
            $this->sheet->getStyle("A{$fila}:N{$fila}")->applyFromArray([
                'fill' => [
                    'fillType' => Fill::FILL_SOLID,
                    'startColor' => ['rgb' => $colorFila],
                ],
                'borders' => [
                    'allBorders' => [
                        'borderStyle' => Border::BORDER_THIN,
                        'color' => ['rgb' => 'D3D3D3'],
                    ],
                ],
            ]);
            
            // Estilo de la columna Estado con color
            $estadoColor = $aprobado ? '00B050' : 'FF0000'; // Verde o Rojo
            $this->sheet->getStyle("M{$fila}")->applyFromArray([
                'font' => [
                    'bold' => true,
                    'color' => ['rgb' => $estadoColor],
                ],
                'alignment' => [
                    'horizontal' => Alignment::HORIZONTAL_CENTER,
                ],
            ]);
            
            // Centrar columnas numéricas
            $this->sheet->getStyle("A{$fila}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            $this->sheet->getStyle("B{$fila}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            $this->sheet->getStyle("F{$fila}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            $this->sheet->getStyle("G{$fila}:L{$fila}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            
            // Formato de números con decimales
            $this->sheet->getStyle("K{$fila}")->getNumberFormat()->setFormatCode('0.00');
            $this->sheet->getStyle("L{$fila}")->getNumberFormat()->setFormatCode('0.00"%"');
            
            $fila++;
        }
        
        // Guardar el rango de datos para estadísticas
        $this->filaFinalDatos = $fila - 1;
        $this->contadorAprobados = $contadorAprobados;
        $this->contadorDesaprobados = $contadorDesaprobados;
        
        // Aplicar filtros automáticos
        $this->sheet->setAutoFilter("A{$filaInicio}:N{$this->filaFinalDatos}");
    }

    protected function crearEstadisticas()
    {
        // ═══════════════════════════════════════════════════════════
        // 📈 RESUMEN ESTADÍSTICO - Después de los datos
        // ═══════════════════════════════════════════════════════════
        
        $filaEstadisticas = $this->filaFinalDatos + 3;
        $total = $this->contadorAprobados + $this->contadorDesaprobados;
        $porcentajeAprobados = $total > 0 ? ($this->contadorAprobados / $total) * 100 : 0;
        
        // Título de estadísticas
        $this->sheet->mergeCells("A{$filaEstadisticas}:N{$filaEstadisticas}");
        $this->sheet->setCellValue("A{$filaEstadisticas}", '📊 RESUMEN ESTADÍSTICO');
        $this->sheet->getStyle("A{$filaEstadisticas}")->applyFromArray([
            'font' => [
                'bold' => true,
                'size' => 14,
                'color' => ['rgb' => 'FFFFFF'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
            ],
            'fill' => [
                'fillType' => Fill::FILL_SOLID,
                'startColor' => ['rgb' => '4472C4'],
            ],
        ]);
        
        $filaEstadisticas++;
        
        // Datos estadísticos
        $estadisticas = [
            ['TOTAL EVALUACIONES', $total],
            ['APROBADOS', $this->contadorAprobados],
            ['DESAPROBADOS', $this->contadorDesaprobados],
            ['% APROBACIÓN', number_format($porcentajeAprobados, 2) . '%'],
        ];
        
        foreach ($estadisticas as $stat) {
            $this->sheet->setCellValue("B{$filaEstadisticas}", $stat[0]);
            $this->sheet->setCellValue("C{$filaEstadisticas}", $stat[1]);
            
            $this->sheet->getStyle("B{$filaEstadisticas}:C{$filaEstadisticas}")->applyFromArray([
                'font' => [
                    'bold' => true,
                    'size' => 12,
                ],
                'fill' => [
                    'fillType' => Fill::FILL_SOLID,
                    'startColor' => ['rgb' => 'E7E6E6'],
                ],
                'borders' => [
                    'allBorders' => [
                        'borderStyle' => Border::BORDER_THIN,
                        'color' => ['rgb' => '000000'],
                    ],
                ],
            ]);
            
            $this->sheet->getStyle("C{$filaEstadisticas}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            
            $filaEstadisticas++;
        }
    }

    protected function ajustarColumnas()
    {
        // Ajustar anchos de columna automáticamente
        $columnas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'];
        foreach ($columnas as $col) {
            $this->sheet->getColumnDimension($col)->setAutoSize(true);
        }
        
        // Establecer ancho mínimo para algunas columnas
        $this->sheet->getColumnDimension('C')->setWidth(40); // Nombres completos
        $this->sheet->getColumnDimension('E')->setWidth(35); // Evento
        $this->sheet->getColumnDimension('N')->setWidth(30); // Observaciones
    }
}
