<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class TiposEventosSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('tipo_eventos')->insert([
            ['id_tipe' => 1, 'nombre' => 'Convocatoria'],
            ['id_tipe' => 2, 'nombre' => 'Cursos'],
            ['id_tipe' => 3, 'nombre' => 'Otros'],
        ]);
    }
}
