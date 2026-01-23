<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class TiposUsuariosSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('tipo_usuarios')->insert([
            ['id_tipu' => 1, 'nombre' => 'administrador'],
            ['id_tipu' => 2, 'nombre' => 'organizador'],
            ['id_tipu' => 3, 'nombre' => 'ayudante'],
        ]);
    }
}
