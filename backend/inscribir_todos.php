<?php

require __DIR__.'/vendor/autoload.php';

$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;

// DNIs a inscribir
$dnis = ['70025674', '72170816'];

// Obtener IDs de personas
$personas = [];
foreach ($dnis as $dni) {
    $persona = DB::table('personas')->where('dni', $dni)->first();
    if ($persona) {
        $personas[$dni] = $persona->id_persona;
        echo "✓ Persona encontrada: DNI {$dni} => ID {$persona->id_persona}\n";
    } else {
        echo "✗ Persona NO encontrada: DNI {$dni}\n";
    }
}

// Obtener todos los eventos
$eventos = DB::table('eventos')->get();
echo "\n📋 Total de eventos: " . count($eventos) . "\n\n";

// Inscribir en cada evento
$inscritos = 0;
$ya_inscritos = 0;

foreach ($eventos as $evento) {
    echo "Evento: {$evento->nombre} (ID: {$evento->id_evento})\n";
    
    foreach ($personas as $dni => $id_persona) {
        // Verificar si ya está inscrito
        $existe = DB::table('inscripciones')
            ->where('evento', $evento->id_evento)
            ->where('persona', $id_persona)
            ->exists();
        
        if (!$existe) {
            DB::table('inscripciones')->insert([
                'evento' => $evento->id_evento,
                'persona' => $id_persona,
                'created_at' => now(),
                'updated_at' => now()
            ]);
            echo "  ✓ Inscrito: DNI {$dni}\n";
            $inscritos++;
        } else {
            echo "  - Ya inscrito: DNI {$dni}\n";
            $ya_inscritos++;
        }
    }
    echo "\n";
}

echo "═══════════════════════════════════════\n";
echo "📊 RESUMEN:\n";
echo "═══════════════════════════════════════\n";
echo "Nuevas inscripciones: {$inscritos}\n";
echo "Ya inscritos: {$ya_inscritos}\n";
echo "Total eventos: " . count($eventos) . "\n";
echo "═══════════════════════════════════════\n";
