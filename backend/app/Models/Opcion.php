<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Opcion extends Model
{
    use HasFactory;

    protected $table = 'opciones';
    protected $primaryKey = 'id_op';
    public $timestamps = true;

    protected $fillable = [
        'id_tipu',
        'nombre',
        'icono',
        'ruta',
    ];
}
