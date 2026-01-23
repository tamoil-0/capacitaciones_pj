<?php

namespace App\Imports;

use App\Models\Evento;
use App\Models\Persona;
use App\Models\Inscripcion;
use Illuminate\Support\Collection;
use Maatwebsite\Excel\Concerns\ToCollection;
use Maatwebsite\Excel\Concerns\WithHeadingRow;
use Illuminate\Support\Str;

class EventPersonImport implements ToCollection, WithHeadingRow
{
    protected $idTipoEvento;

    public function __construct($idTipoEvento)
    {
        $this->idTipoEvento = $idTipoEvento;
    }

    public function collection(Collection $rows)
    {
        // Normalizamos cabeceras a minúsculas sin espacios
        $firstRow = $rows->first();
        $headers = collect($firstRow)->keys()->map(fn($h) => strtolower(trim($h)));

        // Detectamos si hay columnas PLAZA y DEPENDENCIA
        $hasPlaza = $headers->contains('plaza');
        $hasDependencia = $headers->contains('dependencia');

        // Agrupamos filas por evento (PLAZA + DEPENDENCIA)
        $eventGroups = [];

        foreach ($rows as $row) {
            
            $plaza = $row['plaza'] ?? null;
            $dependencia = $row['dependencia'] ?? null;

            // Construir nombre del evento
            $nombreEvento = trim("$plaza - $dependencia");

            // ❌ Si plaza y dependencia están vacíos, NO crear evento vacío
            if ($nombreEvento === '-' || $nombreEvento === '' || $nombreEvento === null) {
                continue;
            }

            // Concatenamos nombre completo
            $nombres = trim(
                implode(' ', array_filter([
                    $row['nom1'] ?? '',
                    $row['nom2'] ?? '',
                    $row['nom3'] ?? ''
                ]))
            );

            $paterno = $row['paterno'] ?? '';
            $materno = $row['materno'] ?? '';
            $dni = isset($row['dni']) ? trim((string)$row['dni']) : null;

            // ✅ Si el DNI tiene 7 dígitos, le agregamos un 0 adelante
            if ($dni && strlen($dni) === 7) {
                $dni = '0' . $dni;
            };

            $eventGroups[$nombreEvento][] = [
                'dni' => $dni,
                'nombres' => $nombres,
                'paterno' => $paterno,
                'materno' => $materno,
            ];
        }

        // Procesamos los grupos
        foreach ($eventGroups as $nombreEvento => $personas) {

            // Buscar o crear el evento
            $evento = Evento::firstOrCreate([
                'nombre' => $nombreEvento,
                'tipo_evento' => $this->idTipoEvento,
            ]);

            // Para cada persona del grupo
            foreach ($personas as $p) {
                if (!$p['dni']) continue; // ignoramos si no hay DNI

                // Buscar o crear persona
                $persona = Persona::firstOrCreate(
                    ['dni' => $p['dni']],
                    [
                        'nombres' => $p['nombres'],
                        'apPaterno' => $p['paterno'],
                        'apMaterno' => $p['materno'],
                    ]
                );

                // Registrar inscripción si no existe
                Inscripcion::firstOrCreate([
                    'evento'   => $evento->id_evento,
                    'persona'  => $persona->id_persona,
                ]);
            }
        }
    }
}