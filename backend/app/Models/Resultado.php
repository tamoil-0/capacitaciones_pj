<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Resultado extends Model
{
    use HasFactory;

    protected $table = 'resultados';
    protected $primaryKey = 'id_resultado';
    public $timestamps = true;

    protected $fillable = [
        'evaluacion',
        'puntaje',
        'total_preguntas',
        'aprobado',
        'archivo_pdf',
        'fecha_calificacion',
    ];

    protected $casts = [
        'fecha_calificacion' => 'datetime',
        'puntaje' => 'decimal:2',
        'aprobado' => 'boolean',
    ];

    /**
     * Relación: Un resultado pertenece a una evaluación
     */
    public function evaluacion()
    {
        return $this->belongsTo(Evaluacion::class, 'evaluacion', 'id_evaluacion');
    }
}
