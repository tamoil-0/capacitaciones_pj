<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Http\Controllers\AuthController;
use App\Http\Controllers\UsuarioController;

use App\Http\Controllers\TipoEventoController;
use App\Http\Controllers\EventoController;

use App\Http\Controllers\PersonaController;
use App\Http\Controllers\InscripcionController;
use App\Http\Controllers\RegistroController;

use App\Http\Controllers\EvaluacionController;

// ════════════════════════════════════════════════════════════════
// ENDPOINTS PARA INTEGRACIÓN OMR - PÚBLICO (sin autenticación)
// ════════════════════════════════════════════════════════════════
Route::prefix('omr')->group(function () {
    // 1. GET /api/omr/eventos - Obtener eventos activos
    Route::get('/eventos', [EvaluacionController::class, 'getEventos']);
    
    // 2. GET /api/omr/eventos/{id}/inscritos - Obtener inscritos de un evento
    Route::get('/eventos/{id}/inscritos', [EvaluacionController::class, 'getInscritos']);
    
    // 3. POST /api/omr/evaluaciones - Crear nueva evaluación
    Route::post('/evaluaciones', [EvaluacionController::class, 'crearEvaluacion']);
    
    // 4. POST /api/omr/resultados - Guardar resultado de evaluación
    Route::post('/resultados', [EvaluacionController::class, 'guardarResultado']);
    
    // 5. POST /api/omr/respuestas - Guardar respuestas OMR detalladas
    Route::post('/respuestas', [EvaluacionController::class, 'guardarRespuestasOmr']);
    
    // 6. GET /api/omr/registros/{id_inscripcion} - Entrada/salida para PDF (público)
    Route::get('/registros/{id_inscripcion}', [RegistroController::class, 'index_x_persona']);
    
    // LEGACY: Mantener compatibilidad con endpoint anterior
    Route::post('/resultado', [EvaluacionController::class, 'guardarResultadoOMR']);
});

Route::post('/login', [AuthController::class, 'login']);

Route::middleware(['auth:sanctum', 'rol:1'])->group(function () {


});

Route::middleware(['auth:sanctum', 'rol:1,2,3'])->group(function () {
    /* ------------------------------------ INICIO PERFIL ------------------------------------ */
        Route::get('/usuario/{id_usuario}',                   [UsuarioController::class, 'show']);
        Route::put('/usuario/{id_usuario}',                   [UsuarioController::class, 'update']);
        Route::post('/usuarios/cambiar-password/{id_usuario}', [UsuarioController::class, 'cambiarPassword']);
    /* ------------------------------------ FIN PERFIL ------------------------------------ */

    
    /* ------------------------------------ INICIO USUARIOS ------------------------------------ */
        // Obtener lista de usuarios
        Route::get('/usuarios',                                    [UsuarioController::class, 'index']);
        // Crear un usuario 
        Route::post('/usuarios',                                   [UsuarioController::class, 'store']);
        // Eliminar un usuario
        Route::delete('/usuarios/{id_usuario}',                    [UsuarioController::class, 'destroy']);
        // Restablecer la contraseña de un usuario
        Route::post('/usuarios/restablecer-password/{id_usuario}', [UsuarioController::class, 'restablecerPassword']);
    /* -------------------------------------- FIN USUARIOS ------------------------------------ */

    /* ------------------------------------ INICIO PERSONAS ------------------------------------ */
        Route::get('/personas',                    [PersonaController::class, 'index']);
        Route::post('/personas',                   [PersonaController::class, 'store']);
        Route::put('/personas/{id_persona}',       [PersonaController::class, 'update']);
        Route::delete('/personas/{id_persona}',    [PersonaController::class, 'destroy']);
    /* --------------------------------------- FIN PERSONAS ------------------------------------ */

    /* ------------------------------------ INICIO TIPO DE EVENTOS ------------------------------------ */
        Route::get('/tipos_eventos', [TipoEventoController::class, 'index']);
    /* ------------------------------------ FIN TIPO DE EVENTOS ------------------------------------ */

    /* ------------------------------------ INICIO EVENTOS ------------------------------------ */
        // Obtener lista de eventos por el tipo al que pertencecen
        Route::get('/eventos/{id_tipo_evento}',  [EventoController::class, 'index']);
        // Crear un nuevo evento
        Route::post('/eventos/{id_tipo_evento}', [EventoController::class, 'store']);
        // Editar un evento
        Route::put('/eventos/{id_evento}',       [EventoController::class, 'update']);
        // Eliminar un evento
        Route::delete('/eventos/{id_evento}',    [EventoController::class, 'destroy']);

        // Importar excel
        Route::post('/eventos/importar-event-person/{id_tipo_evento}',   [EventoController::class, 'importar']);
    /* ------------------------------------ FIN EVENTOS ------------------------------------ */

    /* ------------------------------------ INICIO INSCRITOS ------------------------------------ */
        Route::get('/inscritos/{id_evento}',        [InscripcionController::class, 'index']);
        Route::post('/inscritos/{id_evento}',       [InscripcionController::class, 'store']);
        Route::get('/registros/{id_inscripcion}',   [RegistroController::class, 'index_x_persona']);
        Route::delete('/inscritos/{id_inscrip}',    [InscripcionController::class, 'destroy']);

        // Importar excel
        Route::post('/inscritos/importar-personas/{evento}',   [InscripcionController::class, 'importar']);
        // Tomar asistencia
        Route::post('/registrar/{id_evento}/{dni}',            [RegistroController::class, 'store']);
        // Exportar asistencias a Excel
        Route::get('/registros/exportar/{id_evento?}',         [RegistroController::class, 'exportarAsistencias']);
    /* ------------------------------------ FIN INSCRITOS ------------------------------------ */

    /* ------------------------------------ INICIO EVALUACIONES ------------------------------------ */
        // Obtener todas las evaluaciones con detalles completos
        Route::get('/evaluaciones', [EvaluacionController::class, 'getAllEvaluaciones']);
        // Descargar PDF de evaluación (completo o evidencia)
        Route::get('/evaluaciones/pdf/{id_evento}/{dni}/{tipo}', [EvaluacionController::class, 'descargarPDF']);
        // Exportar evaluaciones a Excel
        Route::get('/evaluaciones/exportar/{id_evento?}', [EvaluacionController::class, 'exportarExcel']);
    /* ------------------------------------ FIN EVALUACIONES ------------------------------------ */

});


