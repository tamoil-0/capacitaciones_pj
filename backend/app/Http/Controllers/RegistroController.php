<?php

namespace App\Http\Controllers;

use App\Models\Persona;
use App\Models\Inscripcion;
use App\Models\Registro;
use App\Models\Evento;
use App\Exports\AsistenciasExcelExport;
use Illuminate\Http\Request;

class RegistroController extends Controller
{
    /**
     * Mostrar todos los registros (asistencias) de una inscripción específica
     */
    public function index_x_persona($id_inscripcion)
    {
        try {
            // Buscar la inscripción para validar que exista
            $inscripcion = Inscripcion::find($id_inscripcion);

            if (!$inscripcion) {
                return response()->json([
                    'message' => 'Inscripción no encontrada.'
                ], 404);
            }

            // Obtener los registros asociados a esa inscripción
            $registros = Registro::where('inscripcion', $id_inscripcion)
                ->orderBy('created_at', 'desc')
                ->get();

            // Si no tiene registros, lo indicamos también
            if ($registros->isEmpty()) {
                return response()->json([
                    'message' => 'No se encontraron registros para esta inscripción.',
                    'registros' => []
                ], 200);
            }

            return response()->json([
                'inscripcion' => $inscripcion->id_inscripcion,
                'persona' => $inscripcion->persona,
                'evento' => $inscripcion->evento,
                'total_registros' => $registros->count(),
                'registros' => $registros
            ], 200);

        } catch (\Exception $e) {
            return response()->json([
                'message' => 'Error al obtener los registros.',
                'error' => $e->getMessage()
            ], 500);
        }
    }


    /**
     * Registrar asistencia según evento y DNI
     * Aplica validación de 30 minutos: registros después de ese tiempo se marcan como TARDANZA
     */
    public function store(Request $request, $id_evento, $dni)
    {
        try {
            // 1️⃣ Buscar persona por DNI
            $persona = Persona::where('dni', $dni)->first();

            if (!$persona) {
                return response()->json([
                    'message' => 'Persona no encontrada con el DNI proporcionado.'
                ], 404);
            }

            // 2️⃣ Buscar inscripción por id_evento + id_persona
            $inscripcion = Inscripcion::where('evento', $id_evento)
                ->where('persona', $persona->id_persona)
                ->first();

            if (!$inscripcion) {
                return response()->json([
                    'message' => 'No se encontró una inscripción para esta persona en el evento.'
                ], 404);
            }

            // 3️⃣ VALIDACIÓN DE DUPLICADOS Y ESTADO ACTUAL
            $tipoRegistro = strtolower($request->tipo ?? 'entrada');
            
            // A) Verificar duplicados en los últimos 30 segundos
            $registroReciente = Registro::where('inscripcion', $inscripcion->id_inscripcion)
                ->where('tipo', $tipoRegistro)
                ->where('created_at', '>=', \Carbon\Carbon::now()->subSeconds(30))
                ->first();

            if ($registroReciente) {
                $segundosTranscurridos = \Carbon\Carbon::now()->diffInSeconds($registroReciente->created_at);
                return response()->json([
                    'message' => 'Esta persona ya registró ' . strtoupper($tipoRegistro) . ' hace ' . $segundosTranscurridos . ' segundos.',
                    'error' => 'DUPLICADO',
                    'persona' => [
                        'nombres' => $persona->nombres,
                        'apPaterno' => $persona->apPaterno,
                        'apMaterno' => $persona->apMaterno,
                        'dni' => $persona->dni
                    ],
                    'ultimo_registro' => $registroReciente->created_at->format('H:i:s')
                ], 409);
            }
            
            // B) Validar estado: NO permitir ENTRADA si ya tiene ENTRADA activa (sin SALIDA)
            if ($tipoRegistro === 'entrada') {
                $ultimaEntrada = Registro::where('inscripcion', $inscripcion->id_inscripcion)
                    ->where('tipo', 'entrada')
                    ->orderBy('created_at', 'desc')
                    ->first();
                
                if ($ultimaEntrada) {
                    // Verificar si hay una salida después de esa entrada
                    $salidaPosterior = Registro::where('inscripcion', $inscripcion->id_inscripcion)
                        ->where('tipo', 'salida')
                        ->where('created_at', '>', $ultimaEntrada->created_at)
                        ->first();
                    
                    if (!$salidaPosterior) {
                        return response()->json([
                            'message' => 'Esta persona ya tiene una ENTRADA registrada sin salida correspondiente. Debe registrar SALIDA primero.',
                            'error' => 'YA_TIENE_ENTRADA',
                            'persona' => [
                                'nombres' => $persona->nombres,
                                'apPaterno' => $persona->apPaterno,
                                'apMaterno' => $persona->apMaterno,
                                'dni' => $persona->dni
                            ],
                            'ultima_entrada' => $ultimaEntrada->created_at->format('d/m/Y H:i:s')
                        ], 409);
                    }
                }
            }
            
            // C) Validar estado: NO permitir SALIDA si no tiene ENTRADA previa
            if ($tipoRegistro === 'salida') {
                $ultimaEntrada = Registro::where('inscripcion', $inscripcion->id_inscripcion)
                    ->where('tipo', 'entrada')
                    ->orderBy('created_at', 'desc')
                    ->first();
                
                if (!$ultimaEntrada) {
                    return response()->json([
                        'message' => 'No se puede registrar SALIDA sin tener una ENTRADA previa.',
                        'error' => 'SIN_ENTRADA_PREVIA',
                        'persona' => [
                            'nombres' => $persona->nombres,
                            'apPaterno' => $persona->apPaterno,
                            'apMaterno' => $persona->apMaterno,
                            'dni' => $persona->dni
                        ]
                    ], 409);
                }
                
                // Verificar si ya tiene salida después de la última entrada
                $salidaPosterior = Registro::where('inscripcion', $inscripcion->id_inscripcion)
                    ->where('tipo', 'salida')
                    ->where('created_at', '>', $ultimaEntrada->created_at)
                    ->first();
                
                if ($salidaPosterior) {
                    return response()->json([
                        'message' => 'Esta persona ya registró SALIDA después de su última entrada.',
                        'error' => 'YA_TIENE_SALIDA',
                        'persona' => [
                            'nombres' => $persona->nombres,
                            'apPaterno' => $persona->apPaterno,
                            'apMaterno' => $persona->apMaterno,
                            'dni' => $persona->dni
                        ],
                        'ultima_salida' => $salidaPosterior->created_at->format('d/m/Y H:i:s')
                    ], 409);
                }
            }

            // 4️⃣ Validar el tipo recibido
            $request->validate([
                'tipo' => 'required|string|max:50',
            ]);

            // 5️⃣ Obtener el evento para validar tiempo SOLO para Convocatorias
            $evento = Evento::with('tipoEvento')->find($id_evento);
            
            // 6️⃣ Para Convocatorias: bloquear entrada después de 30 min
            if ($request->tipo === 'entrada' && $evento && $evento->fecha_evento) {
                // SOLO validar tiempo para tipo Convocatoria (id = 1)
                if ($evento->tipo_evento == 1) {
                    $fechaEvento = \Carbon\Carbon::parse($evento->fecha_evento);
                    $ahora = \Carbon\Carbon::now();
                    $diffMinutos = $fechaEvento->diffInMinutes($ahora, false);
                    
                    // Bloquear entrada si pasaron más de 30 minutos
                    if ($diffMinutos > 30) {
                        return response()->json([
                            'message' => 'Tiempo de entrada vencido. El evento inició hace más de 30 minutos.',
                            'error' => 'TIEMPO_VENCIDO',
                            'minutos_transcurridos' => $diffMinutos
                        ], 403);
                    }
                }
            }

            // 7️⃣ Crear el registro (estado usa default 'A TIEMPO' de la BD)
            $registro = Registro::create([
                'inscripcion' => $inscripcion->id_inscripcion,
                'tipo' => $request->tipo,
            ]);

            return response()->json([
                'message' => 'Registro guardado correctamente.',
                'registro' => $registro,
                'persona' => [
                    'nombres' => $persona->nombres,
                    'apPaterno' => $persona->apPaterno,
                    'apMaterno' => $persona->apMaterno,
                    'dni' => $persona->dni
                ],
                'evento' => $evento ? $evento->nombre : null
            ], 201);

        } catch (\Exception $e) {
            return response()->json([
                'message' => 'Error al registrar la asistencia.',
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT: GET /api/registros/exportar/{id_evento?}
     * Exporta registros de asistencias a Excel con diseño profesional
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function exportarAsistencias($id_evento = null)
    {
        try {
            // Obtener registros con relaciones ANIDADAS correctamente
            $query = Registro::with([
                'inscripcion' => function($q) {
                    $q->with(['personaRel', 'eventoRel.tipoEvento']);
                }
            ]);

            if ($id_evento) {
                $query->whereHas('inscripcion', function($q) use ($id_evento) {
                    $q->where('evento', $id_evento);
                });
            }

            $registros = $query->orderBy('created_at', 'desc')->get();
            
            // Debug: verificar cuántos registros se encontraron
            \Log::info('Total registros encontrados: ' . $registros->count());
            if ($id_evento) {
                \Log::info('Para el evento ID: ' . $id_evento);
            }

            // Obtener información del evento
            $evento = null;
            $tipoEvento = 'Todos';
            $nombreArchivo = 'asistencias_' . now()->format('Y-m-d_H-i-s') . '.xlsx';
            
            if ($id_evento) {
                $evento = Evento::with('tipoEvento')->find($id_evento);
                if ($evento) {
                    $tipoEvento = $evento->tipoEvento->nombre ?? 'General';
                    $nombreEvento = preg_replace('/[^A-Za-z0-9_\-]/', '_', $evento->nombre);
                    $nombreArchivo = 'Asistencias_' . $nombreEvento . '_' . now()->format('Y-m-d_H-i-s') . '.xlsx';
                }
            }

            // Crear directorio si no existe
            $tipoEventoSlug = preg_replace('/[^A-Za-z0-9_\-]/', '_', $tipoEvento);
            $rutaDirectorio = public_path("excel/{$tipoEventoSlug}");
            
            if (!file_exists($rutaDirectorio)) {
                mkdir($rutaDirectorio, 0755, true);
            }

            // Ruta completa del archivo
            $rutaArchivo = "{$rutaDirectorio}/{$nombreArchivo}";
            
            // Crear Excel con diseño profesional
            $export = new AsistenciasExcelExport($registros, $evento, $tipoEvento);
            $export->export($rutaArchivo);

            return response()->json([
                'success' => true,
                'message' => 'Excel de asistencias generado exitosamente',
                'data' => [
                    'nombre_archivo' => $nombreArchivo,
                    'ruta' => "excel/{$tipoEventoSlug}/{$nombreArchivo}",
                    'url' => url("excel/{$tipoEventoSlug}/{$nombreArchivo}"),
                    'tipo_evento' => $tipoEvento,
                    'evento' => $evento ? $evento->nombre : 'Todos los eventos',
                    'total_registros' => $registros->count(),
                ]
            ], 200);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al generar el Excel de asistencias',
                'error' => $e->getMessage(),
                'trace' => config('app.debug') ? $e->getTraceAsString() : null,
            ], 500);
        }
    }
}
