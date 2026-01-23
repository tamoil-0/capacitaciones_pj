<?php

namespace App\Exports;

use App\Models\Evaluacion;
use Maatwebsite\Excel\Concerns\FromCollection;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\WithStyles;
use Maatwebsite\Excel\Concerns\WithColumnWidths;
use Maatwebsite\Excel\Concerns\WithTitle;
use Maatwebsite\Excel\Concerns\WithEvents;
use Maatwebsite\Excel\Events\AfterSheet;
use PhpOffice\PhpSpreadsheet\Worksheet\Worksheet;
use PhpOffice\PhpSpreadsheet\Style\Fill;
use PhpOffice\PhpSpreadsheet\Style\Color;
use PhpOffice\PhpSpreadsheet\Style\Alignment;
use PhpOffice\PhpSpreadsheet\Style\Border;

class EvaluacionesExport implements FromCollection, WithHeadings, WithStyles, WithColumnWidths, WithTitle, WithEvents
{
    protected $idEvento;
    protected $nombreEvento;
    protected $tipoEvento;

    public function __construct($idEvento = null)
    {
        $this->idEvento = $idEvento;
    }

    /**
     * Obtener los datos a exportar
     */
    public function collection()
    {
        $query = Evaluacion::with([
            'inscripcion.persona',
            'inscripcion.evento.tipoEvento',
            'resultado',
            'respuestasOmr'
        ]);

        if ($this->idEvento) {
            $query->whereHas('inscripcion', function($q) {
                $q->where('evento', $this->idEvento);
            });
        }

        $evaluaciones = $query->orderBy('created_at', 'desc')->get();

        // Guardar información del evento para el título
        if ($evaluaciones->isNotEmpty()) {
            $this->nombreEvento = $evaluaciones->first()->inscripcion->evento->nombre ?? 'Todos';
            $this->tipoEvento = $evaluaciones->first()->inscripcion->evento->tipoEvento->nombre ?? 'N/A';
        }

        return $evaluaciones->map(function ($evaluacion, $index) {
            $persona = $evaluacion->inscripcion->persona;
            $resultado = $evaluacion->resultado;
            $evento = $evaluacion->inscripcion->evento;
            
            // Contar respuestas
            $totalPreguntas = $resultado->total_preguntas ?? 0;
            $correctas = $resultado->correctas ?? 0;
            $incorrectas = $resultado->incorrectas ?? 0;
            $enBlanco = $totalPreguntas - ($correctas + $incorrectas);

            return [
                $index + 1,                                             // N°
                $persona->dni,                                          // DNI
                trim($persona->nombres . ' ' . $persona->apPaterno . ' ' . $persona->apMaterno), // Nombres Completos
                $evento->tipoEvento->nombre ?? 'N/A',                  // Tipo de Evento
                $evento->nombre,                                        // Nombre del Evento
                $evaluacion->fecha_evaluacion->format('d/m/Y H:i'),   // Fecha de Evaluación
                $totalPreguntas,                                        // Total Preguntas
                $correctas,                                             // Correctas
                $incorrectas,                                           // Incorrectas
                $enBlanco,                                              // En Blanco
                number_format($resultado->puntaje ?? 0, 2),            // Puntaje
                number_format($resultado->porcentaje ?? 0, 2),         // Nota (%)
                $resultado->aprobado ? 'APROBADO' : 'DESAPROBADO',     // Estado
                $evaluacion->observaciones ?? '-',                      // Observaciones
            ];
        });
    }

    /**
     * Encabezados de las columnas
     */
    public function headings(): array
    {
        return [
            'N°',
            'DNI',
            'NOMBRES COMPLETOS',
            'TIPO DE EVENTO',
            'EVENTO',
            'FECHA EVALUACIÓN',
            'TOTAL PREGUNTAS',
            'CORRECTAS',
            'INCORRECTAS',
            'EN BLANCO',
            'PUNTAJE',
            'NOTA (%)',
            'ESTADO',
            'OBSERVACIONES',
        ];
    }

    /**
     * Estilos de la hoja
     */
    public function styles(Worksheet $sheet)
    {
        return [
            // Estilo del encabezado (fila 1)
            1 => [
                'font' => [
                    'bold' => true,
                    'color' => ['rgb' => 'FFFFFF'],
                    'size' => 11,
                ],
                'fill' => [
                    'fillType' => Fill::FILL_SOLID,
                    'startColor' => ['rgb' => '1E40AF'], // Azul oscuro
                ],
                'alignment' => [
                    'horizontal' => Alignment::HORIZONTAL_CENTER,
                    'vertical' => Alignment::VERTICAL_CENTER,
                ],
                'borders' => [
                    'allBorders' => [
                        'borderStyle' => Border::BORDER_THIN,
                        'color' => ['rgb' => '000000'],
                    ],
                ],
            ],
        ];
    }

    /**
     * Ancho de las columnas
     */
    public function columnWidths(): array
    {
        return [
            'A' => 6,   // N°
            'B' => 12,  // DNI
            'C' => 35,  // Nombres
            'D' => 25,  // Tipo Evento
            'E' => 30,  // Evento
            'F' => 18,  // Fecha
            'G' => 14,  // Total Preguntas
            'H' => 11,  // Correctas
            'I' => 11,  // Incorrectas
            'J' => 11,  // En Blanco
            'K' => 10,  // Puntaje
            'L' => 10,  // Nota
            'M' => 14,  // Estado
            'N' => 30,  // Observaciones
        ];
    }

    /**
     * Título de la hoja
     */
    public function title(): string
    {
        return 'Evaluaciones';
    }

    /**
     * Eventos personalizados para formato avanzado
     */
    public function registerEvents(): array
    {
        return [
            AfterSheet::class => function(AfterSheet $event) {
                $sheet = $event->sheet->getDelegate();
                $highestRow = $sheet->getHighestRow();
                $highestColumn = $sheet->getHighestColumn();

                // Ajustar altura de la fila de encabezado
                $sheet->getRowDimension(1)->setRowHeight(25);

                // Aplicar bordes a todas las celdas con datos
                $sheet->getStyle("A1:{$highestColumn}{$highestRow}")
                    ->getBorders()
                    ->getAllBorders()
                    ->setBorderStyle(Border::BORDER_THIN)
                    ->setColor(new Color('CCCCCC'));

                // Centrar columnas específicas
                $centerColumns = ['A', 'B', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'];
                foreach ($centerColumns as $col) {
                    $sheet->getStyle("{$col}2:{$col}{$highestRow}")
                        ->getAlignment()
                        ->setHorizontal(Alignment::HORIZONTAL_CENTER)
                        ->setVertical(Alignment::VERTICAL_CENTER);
                }

                // Aplicar colores alternados a las filas
                for ($row = 2; $row <= $highestRow; $row++) {
                    if ($row % 2 == 0) {
                        $sheet->getStyle("A{$row}:{$highestColumn}{$row}")
                            ->getFill()
                            ->setFillType(Fill::FILL_SOLID)
                            ->setStartColor(new Color('F3F4F6')); // Gris claro
                    }
                }

                // Aplicar color verde a APROBADO y rojo a DESAPROBADO
                for ($row = 2; $row <= $highestRow; $row++) {
                    $cellValue = $sheet->getCell("M{$row}")->getValue();
                    
                    if ($cellValue === 'APROBADO') {
                        $sheet->getStyle("M{$row}")
                            ->getFont()
                            ->setBold(true)
                            ->setColor(new Color('047857')); // Verde oscuro
                        
                        $sheet->getStyle("M{$row}")
                            ->getFill()
                            ->setFillType(Fill::FILL_SOLID)
                            ->setStartColor(new Color('D1FAE5')); // Verde claro
                    } elseif ($cellValue === 'DESAPROBADO') {
                        $sheet->getStyle("M{$row}")
                            ->getFont()
                            ->setBold(true)
                            ->setColor(new Color('B91C1C')); // Rojo oscuro
                        
                        $sheet->getStyle("M{$row}")
                            ->getFill()
                            ->setFillType(Fill::FILL_SOLID)
                            ->setStartColor(new Color('FEE2E2')); // Rojo claro
                    }
                }

                // Auto-ajustar la altura de las filas de datos
                for ($row = 2; $row <= $highestRow; $row++) {
                    $sheet->getRowDimension($row)->setRowHeight(-1); // Auto
                }

                // Congelar la fila de encabezados
                $sheet->freezePane('A2');
            },
        ];
    }
}
