<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class UsuariosSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Usuario Administrador Principal - Poder Judicial
        DB::table('usuarios')->insert([
            [
                'id_usuario' => 1,
                'nombres_apellidos' => 'Corte Superior de Justicia de Puno',
                'nickname' => 'pjudicial',
                'contrasena' => '$2y$10$Ar9Xn6hh.gEaa1dk1.DbJ.jVN56Ni0LFf3v1UmPtU82s49EY/q7rG', // Contraseña: Corte2026
                'tipo_usuario' => 1,
                'asignado' => null,
                'habilitado' => 1,
            ],
        ]);
    }
}
