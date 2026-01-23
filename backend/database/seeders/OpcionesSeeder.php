<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class OpcionesSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Limpiar tabla antes de insertar
        DB::table('opciones')->truncate();
        
        DB::table('opciones')->insert([
            ['id_op' => 1, 'id_tipu' => 1, 'nombre' => 'Eventos',   'icono' => 'mdi-certificate',   'ruta' => '/tipos_eventos'],   
            ['id_op' => 2, 'id_tipu' => 1, 'nombre' => 'Usuarios',  'icono' => 'mdi-account-tie',   'ruta' => '/usuarios'],   
            ['id_op' => 3, 'id_tipu' => 1, 'nombre' => 'Personas',  'icono' => 'mdi-account',       'ruta' => '/personas'], 
            
            ['id_op' => 4, 'id_tipu' => 2, 'nombre' => 'Eventos',   'icono' => 'mdi-certificate',   'ruta' => '/eventos/'],   
            ['id_op' => 5, 'id_tipu' => 2, 'nombre' => 'Usuarios',  'icono' => 'mdi-account',       'ruta' => '/usuarios'],
            
            ['id_op' => 6, 'id_tipu' => 3, 'nombre' => 'Eventos',   'icono' => 'mdi-certificate',   'ruta' => '/eventos/'],
        ]);
    }
}
