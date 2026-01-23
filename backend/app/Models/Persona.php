<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Persona extends Model
{
    use HasFactory;

    protected $table = 'personas';
    protected $primaryKey = 'id_persona';
    public $timestamps = true;

    protected $fillable = [
        'dni', 
        'nombres', 
        'apPaterno', 
        'apMaterno'
    ];

    public function inscripciones()
    {
        return $this->hasMany(Inscripcion::class, 'persona', 'id_persona');
    }
}