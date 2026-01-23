<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class RespuestaOmr extends Model
{
    use HasFactory;

    protected $table = 'respuestas_omr';
    protected $primaryKey = 'id_respuesta_omr';
    public $timestamps = true;

    protected $fillable = [
        'evaluacion',
        'numero_pregunta',
        'respuesta_marcada',
        'confianza',
    ];

    protected $casts = [
        'numero_pregunta' => 'integer',
        'confianza' => 'decimal:2',
    ];

    /**
     * Relación: Una respuesta OMR pertenece a una evaluación
     */
    public function evaluacion()
    {
        return $this->belongsTo(Evaluacion::class, 'evaluacion', 'id_evaluacion');
    }
}
