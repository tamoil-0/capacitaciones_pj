<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('inscripciones', function (Blueprint $table) {
            $table->id('id_inscripcion');
            $table->unsignedBigInteger('evento');
            $table->unsignedBigInteger('persona');
            $table->timestamps();

            $table->foreign('evento')->references('id_evento')->on('eventos')->onDelete('cascade');
            $table->foreign('persona')->references('id_persona')->on('personas')->onDelete('cascade');
        });

        Schema::create('registros', function (Blueprint $table) {
            $table->id('id_registro');
            $table->unsignedBigInteger('inscripcion');
            $table->string('tipo', 50);
            $table->timestamps();

            $table->foreign('inscripcion')->references('id_inscripcion')->on('inscripciones')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('registros_io');
        Schema::dropIfExists('inscripciones');
    }
};
