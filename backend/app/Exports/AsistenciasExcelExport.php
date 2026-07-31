<?php

namespace App\Exports;

use App\Models\Inscripcion;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;
use PhpOffice\PhpSpreadsheet\Style\Alignment;
use PhpOffice\PhpSpreadsheet\Style\Border;
use PhpOffice\PhpSpreadsheet\Style\Fill;
use PhpOffice\PhpSpreadsheet\Style\Color;

class AsistenciasExcelExport
{
    protected $registros;
    protected $evento;
    protected $tipoEvento;
    protected $spreadsheet;
    protected $sheet;

    public function __construct($registros, $evento = null, $tipoEvento = 'Todos')
    {
        $this->registros = $registros;
        $this->evento = $evento;
        $this->tipoEvento = $tipoEvento;
    }

    public function export($rutaArchivo)
    {
        $this->spreadsheet = new Spreadsheet();
        $this->sheet = $this->spreadsheet->getActiveSheet();
        
        // Configurar hoja
        $this->sheet->setTitle('Asistencias');
        
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
        // 📋 ENCABEZADO PRINCIPAL
        // ═══════════════════════════════════════════════════════════
        
        $margin = 1;
        
        // Fila 1-2: Título principal
        $this->sheet->mergeCells('A1:L2');
        $this->sheet->setCellValue('A1', 'SISTEMA DE ASISTENCIA Y CALIFICACIÓN DE EXÁMENES - REPORTE DE ASISTENCIAS');
        $this->sheet->getStyle('A1')->applyFromArray([
            'font' => [
                'bold' => true,
                'size' => 16,
                'color' => ['rgb' => 'FFFFFF'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
                'vertical' => Alignment::VERTICAL_CENTER,
            ],
            'fill' => [
                'fillType' => Fill::FILL_SOLID,
                'startColor' => ['rgb' => '0D47A1'], // Azul oscuro profesional
            ],
        ]);
        
        // Fila 3: Información del evento
        $this->sheet->mergeCells('A3:L3');
        $eventoNombre = $this->evento ? $this->evento->nombre : 'Todos los eventos';
        $this->sheet->setCellValue('A3', "Evento: {$eventoNombre} | Tipo: {$this->tipoEvento}");
        $this->sheet->getStyle('A3')->applyFromArray([
            'font' => [
                'bold' => true,
                'size' => 12,
                'color' => ['rgb' => '1565C0'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
            ],
            'fill' => [
                'fillType' => Fill::FILL_SOLID,
                'startColor' => ['rgb' => 'E3F2FD'],
            ],
        ]);
        
        // Fila 4: Fecha de generación
        $this->sheet->mergeCells('A4:L4');
        $this->sheet->setCellValue('A4', 'Generado: ' . now()->format('d/m/Y H:i:s'));
        $this->sheet->getStyle('A4')->applyFromArray([
            'font' => [
                'italic' => true,
                'size' => 10,
                'color' => ['rgb' => '757575'],
            ],
            'alignment' => [
                'horizontal' => Alignment::HORIZONTAL_CENTER,
            ],
        ]);
        
        // Establecer altura de filas
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
            'F' => 'FECHA',
            'G' => 'HORA ENTRADA',
            'H' => 'HORA SALIDA',
            'I' => 'ASISTIÓ',
            'J' => 'OBSERVACIONES',
        ];
        
        foreach ($encabezados as $col => $titulo) {
            $this->sheet->setCellValue("{$col}{$filaInicio}", $titulo);
        }
        
        // Estilo de encabezados
        $this->sheet->getStyle("A{$filaInicio}:J{$filaInicio}")->applyFromArray([
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
                'startColor' => ['rgb' => '1976D2'],
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
        // 📝 DATOS DE LOS REGISTROS - AGRUPADOS POR PERSONA
        // ═══════════════════════════════════════════════════════════
        
        $fila = $filaInicio + 1;
        $totalEntradas = 0;
        $totalSalidas = 0;
        
        // Agrupar registros por inscripción (persona)
        $registrosAgrupados = [];
        foreach ($this->registros as $registro) {
            $inscripcionId = $registro->inscripcion;
            if (!isset($registrosAgrupados[$inscripcionId])) {
                $registrosAgrupados[$inscripcionId] = [
                    'inscripcion' => $inscripcionId,
                    'entradas' => [],
                    'salidas' => [],
                ];
            }
            
            $tipoRegistro = strtolower($registro->tipo ?? '');
            if ($tipoRegistro === 'entrada') {
                $registrosAgrupados[$inscripcionId]['entradas'][] = $registro;
                $totalEntradas++;
            } elseif ($tipoRegistro === 'salida') {
                $registrosAgrupados[$inscripcionId]['salidas'][] = $registro;
                $totalSalidas++;
            }
        }
        
        $numeroFila = 1;
        foreach ($registrosAgrupados as $inscripcionId => $datos) {
            try {
                // Cargar inscripción con sus relaciones
                $inscripcionObj = Inscripcion::with(['personaRel', 'eventoRel.tipoEvento'])
                    ->find($inscripcionId);
                
                if (!$inscripcionObj) {
                    continue;
                }
                
                $persona = $inscripcionObj->personaRel;
                $evento = $inscripcionObj->eventoRel;
                
                // Si no hay datos esenciales, saltar
                if (!$persona || !$evento) {
                    continue;
                }
                
                // Obtener última entrada y última salida
                $ultimaEntrada = !empty($datos['entradas']) ? end($datos['entradas']) : null;
                $ultimaSalida = !empty($datos['salidas']) ? end($datos['salidas']) : null;
                
                // Determinar si asistió (tiene entrada o salida)
                $asistio = ($ultimaEntrada || $ultimaSalida) ? 'SÍ' : 'NO';
                $asistioColor = '00B050'; // Verde siempre
                
                // Datos de la fila
                $this->sheet->setCellValue("A{$fila}", $numeroFila);
                $this->sheet->setCellValue("B{$fila}", $persona->dni ?? 'N/A');
                
                // Concatenar nombres correctamente
                $nombreCompleto = trim(
                    ($persona->apPaterno ?? '') . ' ' . 
                    ($persona->apMaterno ?? '') . ' ' . 
                    ($persona->nombres ?? '')
                );
                $nombreCompleto = $nombreCompleto ?: 'Sin nombre';
                $this->sheet->setCellValue("C{$fila}", $nombreCompleto);
                
                $this->sheet->setCellValue("D{$fila}", $evento->tipoEvento->nombre ?? 'N/A');
                $this->sheet->setCellValue("E{$fila}", $evento->nombre ?? 'N/A');
                
                // Obtener fecha (de entrada o salida, lo que esté disponible)
                $fechaRegistro = $ultimaEntrada ? $ultimaEntrada->created_at : ($ultimaSalida ? $ultimaSalida->created_at : null);
                $this->sheet->setCellValue("F{$fila}", $fechaRegistro ? $fechaRegistro->format('d/m/Y') : 'N/A');
                
                // HORA DE ENTRADA
                $horaEntrada = $ultimaEntrada ? $ultimaEntrada->created_at->format('H:i:s') : '-';
                $this->sheet->setCellValue("G{$fila}", $horaEntrada);
                
                // HORA DE SALIDA
                $horaSalida = $ultimaSalida ? $ultimaSalida->created_at->format('H:i:s') : '-';
                $this->sheet->setCellValue("H{$fila}", $horaSalida);
                
                $this->sheet->setCellValue("I{$fila}", $asistio);
                $this->sheet->setCellValue("J{$fila}", '-');
            
            // Estilo de datos - Filas alternadas
            $colorFila = ($fila % 2 == 0) ? 'F5F5F5' : 'FFFFFF';
            $this->sheet->getStyle("A{$fila}:J{$fila}")->applyFromArray([
                'fill' => [
                    'fillType' => Fill::FILL_SOLID,
                    'startColor' => ['rgb' => $colorFila],
                ],
                'borders' => [
                    'allBorders' => [
                        'borderStyle' => Border::BORDER_THIN,
                        'color' => ['rgb' => 'E0E0E0'],
                    ],
                ],
            ]);
            
            // Estilo de la columna Asistió con color verde
            $this->sheet->getStyle("I{$fila}")->applyFromArray([
                'font' => [
                    'bold' => true,
                    'color' => ['rgb' => $asistioColor],
                ],
                'alignment' => [
                    'horizontal' => Alignment::HORIZONTAL_CENTER,
                ],
            ]);
            
            // Estilo para horas - Verde para entrada, Naranja para salida
            if ($horaEntrada !== '-') {
                $this->sheet->getStyle("G{$fila}")->applyFromArray([
                    'font' => [
                        'bold' => true,
                        'color' => ['rgb' => '4CAF50'], // Verde
                    ],
                    'alignment' => [
                        'horizontal' => Alignment::HORIZONTAL_CENTER,
                    ],
                ]);
            }
            
            if ($horaSalida !== '-') {
                $this->sheet->getStyle("H{$fila}")->applyFromArray([
                    'font' => [
                        'bold' => true,
                        'color' => ['rgb' => 'FF9800'], // Naranja
                    ],
                    'alignment' => [
                        'horizontal' => Alignment::HORIZONTAL_CENTER,
                    ],
                ]);
            }
            
            // Centrar columnas
            $this->sheet->getStyle("A{$fila}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            $this->sheet->getStyle("B{$fila}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            $this->sheet->getStyle("F{$fila}")->getAlignment()->setHorizontal(Alignment::HORIZONTAL_CENTER);
            
            $fila++;
            $numeroFila++;
            } catch (\Exception $e) {
                // Si hay error en un registro, saltar al siguiente
                continue;
            }
        }
        
        // Guardar datos para estadísticas
        $this->filaFinalDatos = $fila - 1;
        $this->totalEntradas = $totalEntradas;
        $this->totalSalidas = $totalSalidas;
        $this->totalOtros = 0;
        
        // Aplicar filtros automáticos
        $this->sheet->setAutoFilter("A{$filaInicio}:J{$this->filaFinalDatos}");
    }

    protected function crearEstadisticas()
    {
        // ═══════════════════════════════════════════════════════════
        // 📈 RESUMEN ESTADÍSTICO
        // ═══════════════════════════════════════════════════════════
        
        $filaEstadisticas = $this->filaFinalDatos + 3;
        $total = $this->totalEntradas + $this->totalSalidas + $this->totalOtros;
        
        // Título
        $this->sheet->mergeCells("A{$filaEstadisticas}:J{$filaEstadisticas}");
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
                'startColor' => ['rgb' => '1976D2'],
            ],
        ]);
        
        $filaEstadisticas++;
        
        // Datos estadísticos
        $estadisticas = [
            ['TOTAL REGISTROS', $total],
            ['TOTAL ENTRADAS', $this->totalEntradas],
            ['TOTAL SALIDAS', $this->totalSalidas],
            ['OTROS REGISTROS', $this->totalOtros],
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
                    'startColor' => ['rgb' => 'E3F2FD'],
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
        // Ajustar anchos de columna
        $this->sheet->getColumnDimension('A')->setWidth(8);  // N°
        $this->sheet->getColumnDimension('B')->setWidth(12); // DNI
        $this->sheet->getColumnDimension('C')->setWidth(40); // Nombres
        $this->sheet->getColumnDimension('D')->setWidth(18); // Tipo Evento
        $this->sheet->getColumnDimension('E')->setWidth(35); // Evento
        $this->sheet->getColumnDimension('F')->setWidth(15); // Tipo Registro
        $this->sheet->getColumnDimension('G')->setWidth(12); // Fecha
        $this->sheet->getColumnDimension('H')->setWidth(10); // Hora
        $this->sheet->getColumnDimension('I')->setWidth(12); // Estado
        $this->sheet->getColumnDimension('J')->setWidth(25); // Observaciones
    }
}
