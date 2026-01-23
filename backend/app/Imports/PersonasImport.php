<?php

namespace App\Imports;

use App\Models\Persona;
use App\Models\Inscripcion;
use Maatwebsite\Excel\Concerns\ToModel;
use Maatwebsite\Excel\Concerns\WithHeadingRow;

class PersonasImport implements ToModel, WithHeadingRow
{
    protected $eventoId;

    public function __construct($eventoId)
    {
        $this->eventoId = $eventoId;
    }

    public function model(array $row)
    {
        // Buscar o crear persona por DNI
        $persona = Persona::firstOrCreate(
            ['dni' => $row['dni']],
            [
                'nombres' => $row['nombres'],
                'apPaterno' => $row['Paterno'],
                'apMaterno' => $row['Materno'],
            ]
        );

        // Registrar inscripción si no existe
        Inscripcion::firstOrCreate([
            'evento'   => $this->eventoId,
            'persona'  => $persona->id_persona,
        ]);

        return $persona;
    }
}
