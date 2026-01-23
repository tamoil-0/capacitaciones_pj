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
        Schema::create('tipo_eventos', function (Blueprint $table) {
            $table->id('id_tipe');
            $table->string('nombre', 255);
        });

        Schema::create('eventos', function (Blueprint $table) {
            $table->id('id_evento');
            $table->string('nombre', 255);
            $table->dateTime('fecha_evento')->nullable();
            $table->unsignedBigInteger('tipo_evento');
            $table->boolean('estado')->default(0);
            $table->timestamp('fecha_creacion')->useCurrent();

            $table->foreign('tipo_evento')->references('id_tipe')->on('tipo_eventos')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('eventos');
        Schema::dropIfExists('tipo_eventos');
    }
};
