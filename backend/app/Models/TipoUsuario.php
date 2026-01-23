<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TipoUsuario extends Model
{
    use HasFactory;

    protected $table = 'tipo_usuarios';
    protected $primaryKey = 'id_tipu';
    public $timestamps = true;

    protected $fillable = [
        'nombre',
    ];
}
