<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Inscripcion extends Model
{
    use HasFactory;

    protected $table = 'inscripciones';
    protected $primaryKey = 'id_inscripcion';
    public $timestamps = true;

    protected $fillable = [
        'persona',
        'evento',
    ];

    public function persona()
    {
        return $this->belongsTo(Persona::class, 'persona', 'id_persona');
    }

    public function personaRel()
    {
        return $this->belongsTo(Persona::class, 'persona', 'id_persona');
    }

    public function evento()
    {
        return $this->belongsTo(Evento::class, 'evento', 'id_evento');
    }

    public function eventoRel()
    {
        return $this->belongsTo(Evento::class, 'evento', 'id_evento');
    }

    public function registros()
    {
        return $this->hasMany(Registro::class, 'inscripcion', 'id_inscripcion');
    }

    /**
     * Relación: Una inscripción tiene MUCHAS evaluaciones (NUEVO)
     */
    public function evaluaciones()
    {
        return $this->hasMany(Evaluacion::class, 'inscripcion', 'id_inscripcion');
    }
}
