<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Evento extends Model
{
    use HasFactory;

    protected $table = 'eventos';
    protected $primaryKey = 'id_evento';
    public $timestamps = false;

    protected $fillable = [
        'nombre',
        'fecha_evento',
        'tipo_evento',
        'estado',
        'fecha_creacion',

    ];

    // Si quieres que fecha_evento y fecha_creacion se manejen como fechas
    protected $casts = [
        'fecha_evento'   => 'datetime',
        'fecha_creacion' => 'datetime',
    ];

    // Relaciones
    public function tipoEvento()
    {
        return $this->belongsTo(TipoEvento::class, 'tipo_evento', 'id_tipe');
    }

}
