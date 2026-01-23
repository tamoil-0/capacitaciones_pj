<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Evaluacion extends Model
{
    use HasFactory;

    protected $table = 'evaluaciones';
    protected $primaryKey = 'id_evaluacion';
    public $timestamps = true;

    protected $fillable = [
        'inscripcion',
        'fecha_evaluacion',
        'tipo_examen',
        'estado',
        'observaciones',
    ];

    protected $casts = [
        'fecha_evaluacion' => 'datetime',
    ];

    /**
     * Relación: Una evaluación pertenece a una inscripción
     */
    public function inscripcion()
    {
        return $this->belongsTo(Inscripcion::class, 'inscripcion', 'id_inscripcion');
    }

    /**
     * Alias para usar con eager loading
     */
    public function inscripcionRel()
    {
        return $this->belongsTo(Inscripcion::class, 'inscripcion', 'id_inscripcion');
    }

    /**
     * Relación: Una evaluación tiene UN resultado
     */
    public function resultado()
    {
        return $this->hasOne(Resultado::class, 'evaluacion', 'id_evaluacion');
    }

    /**
     * Alias para usar con eager loading
     */
    public function resultadoRel()
    {
        return $this->hasOne(Resultado::class, 'evaluacion', 'id_evaluacion');
    }

    /**
     * Relación: Una evaluación tiene MUCHAS respuestas OMR
     */
    public function respuestasOmr()
    {
        return $this->hasMany(RespuestaOmr::class, 'evaluacion', 'id_evaluacion');
    }
}
