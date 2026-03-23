<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * Hora inicio = fecha_evento (creación del evento).
     * Hora fin = fecha_fin (cuando el estado pasa a Finalizado).
     */
    public function up(): void
    {
        Schema::table('eventos', function (Blueprint $table) {
            $table->dateTime('fecha_fin')->nullable()->after('fecha_evento');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('eventos', function (Blueprint $table) {
            $table->dropColumn('fecha_fin');
        });
    }
};
