<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * 
     * Tabla: evaluaciones
     * Relación: Una inscripción puede tener MUCHAS evaluaciones
     * (permite evaluar múltiples veces al mismo inscrito en el mismo evento)
     */
    public function up(): void
    {
        Schema::create('evaluaciones', function (Blueprint $table) {
            $table->id('id_evaluacion');
            $table->unsignedBigInteger('inscripcion');
            $table->dateTime('fecha_evaluacion');
            $table->string('tipo_examen', 50)->default('regular'); // regular, recuperacion, etc.
            $table->enum('estado', ['valida', 'invalida', 'anulada'])->default('valida');
            $table->text('observaciones')->nullable();
            $table->timestamps();

            $table->foreign('inscripcion')
                  ->references('id_inscripcion')
                  ->on('inscripciones')
                  ->onDelete('cascade');
        });

        Schema::create('resultados', function (Blueprint $table) {
            $table->id('id_resultado');
            $table->unsignedBigInteger('evaluacion');
            $table->decimal('puntaje', 5, 2); // ej: 85.50
            $table->integer('total_preguntas')->default(30);
            $table->boolean('aprobado')->default(false);
            $table->string('archivo_pdf', 500)->nullable();
            $table->dateTime('fecha_calificacion');
            $table->timestamps();

            $table->foreign('evaluacion')
                  ->references('id_evaluacion')
                  ->on('evaluaciones')
                  ->onDelete('cascade');
        });

        Schema::create('respuestas_omr', function (Blueprint $table) {
            $table->id('id_respuesta_omr');
            $table->unsignedBigInteger('evaluacion');
            $table->integer('numero_pregunta'); // 1 a 30
            $table->string('respuesta_marcada', 10)->nullable(); // A, B, C, D, E, null
            $table->decimal('confianza', 5, 2)->nullable(); // % de confianza del OMR
            $table->timestamps();

            $table->foreign('evaluacion')
                  ->references('id_evaluacion')
                  ->on('evaluaciones')
                  ->onDelete('cascade');

            // Índice compuesto para búsquedas rápidas
            $table->unique(['evaluacion', 'numero_pregunta']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('respuestas_omr');
        Schema::dropIfExists('resultados');
        Schema::dropIfExists('evaluaciones');
    }
};
