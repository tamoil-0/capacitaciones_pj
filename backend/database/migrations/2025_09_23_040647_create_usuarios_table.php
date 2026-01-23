<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tipo_usuarios', function (Blueprint $table) {
            $table->id('id_tipu');
            $table->string('nombre', 50);
            $table->timestamps();
        });

        Schema::create('usuarios', function (Blueprint $table) {
            $table->id('id_usuario');
            $table->string('nombres_apellidos', 255);
            $table->string('nickname', 50)->unique();
            $table->string('contrasena', 255);
            $table->unsignedBigInteger('tipo_usuario');
            $table->unsignedBigInteger('asignado')->nullable();
            $table->boolean('habilitado')->default(0);
            $table->timestamps();

            $table->foreign('tipo_usuario')->references('id_tipu')->on('tipo_usuarios')->onDelete('cascade');
        });

        Schema::create('opciones', function (Blueprint $table) {
            $table->id('id_op');
            $table->unsignedBigInteger('id_tipu');
            $table->string('nombre', 100);
            $table->string('icono', 100);
            $table->string('ruta', 255);
            $table->timestamps();

            $table->foreign('id_tipu')->references('id_tipu')->on('tipo_usuarios')->onDelete('cascade');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('opciones');
        Schema::dropIfExists('usuarios');
        Schema::dropIfExists('tipo_usuarios');
    }
};
