<?php

namespace App\Http\Controllers;

use App\Models\Persona;
use App\Models\Inscripcion;
use App\Models\Evaluacion;
use App\Models\Resultado;
use App\Models\RespuestaOmr;
use App\Models\Evento;
use App\Exports\EvaluacionesExcelExport;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class EvaluacionController extends Controller
{
    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT 1: GET /api/eventos
     * Devuelve la lista de eventos activos para el OMR
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function getEventos()
    {
        $eventos = Evento::where('estado', 1)
            ->select('id_evento', 'nombre', 'fecha_evento', 'tipo_evento')
            ->orderBy('fecha_evento', 'desc')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $eventos
        ], 200);
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT 2: GET /api/eventos/{id}/inscritos
     * Devuelve los inscritos (DNI + id_inscripcion)
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function getInscritos($id_evento)
    {
        $inscritos = Inscripcion::where('evento', $id_evento)
            ->join('personas', 'inscripciones.persona', '=', 'personas.id_persona')
            ->select(
                'inscripciones.id_inscripcion',
                'personas.dni',
                'personas.nombres',
                'personas.apPaterno',
                'personas.apMaterno'
            )
            ->get();

        return response()->json([
            'success' => true,
            'evento_id' => $id_evento,
            'total_inscritos' => $inscritos->count(),
            'data' => $inscritos
        ], 200);
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT 3: POST /api/evaluaciones
     * Crea una nueva evaluación
     * Body: { "id_inscripcion": 123, "tipo_examen": "regular" }
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function crearEvaluacion(Request $request)
    {
        $request->validate([
            'id_inscripcion' => 'required|exists:inscripciones,id_inscripcion',
            'tipo_examen' => 'nullable|string|max:50',
            'observaciones' => 'nullable|string',
        ]);

        $evaluacion = Evaluacion::create([
            'inscripcion' => $request->id_inscripcion,
            'fecha_evaluacion' => now(),
            'tipo_examen' => $request->tipo_examen ?? 'regular',
            'estado' => 'valida',
            'observaciones' => $request->observaciones,
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Evaluación creada exitosamente',
            'data' => [
                'id_evaluacion' => $evaluacion->id_evaluacion,
                'inscripcion' => $evaluacion->inscripcion,
                'fecha_evaluacion' => $evaluacion->fecha_evaluacion,
            ]
        ], 201);
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT 4: POST /api/resultados
     * Guarda el resultado de una evaluación
     * Body: {
     *   "id_evaluacion": 123,
     *   "puntaje": 85.50,
     *   "total_preguntas": 30,
     *   "aprobado": true,
     *   "archivo_pdf": "resultados_omr/12345678_resultado.pdf"
     * }
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function guardarResultado(Request $request)
    {
        $request->validate([
            'id_evaluacion' => 'required|exists:evaluaciones,id_evaluacion',
            'puntaje' => 'required|numeric|min:0',
            'total_preguntas' => 'required|integer|min:1',
            'aprobado' => 'required|boolean',
            'archivo_pdf' => 'nullable|string|max:500',
        ]);

        $resultado = Resultado::updateOrCreate(
            ['evaluacion' => $request->id_evaluacion],
            [
                'puntaje' => $request->puntaje,
                'total_preguntas' => $request->total_preguntas,
                'aprobado' => $request->puntaje >= 20, // FORZAR: Aprobado si puntaje >= 20
                'archivo_pdf' => $request->archivo_pdf,
                'fecha_calificacion' => now(),
            ]
        );

        return response()->json([
            'success' => true,
            'message' => 'Resultado guardado exitosamente',
            'data' => [
                'id_resultado' => $resultado->id_resultado,
                'id_evaluacion' => $resultado->evaluacion,
                'puntaje' => $resultado->puntaje,
                'aprobado' => $resultado->aprobado,
            ]
        ], 201);
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT 5: POST /api/respuestas-omr
     * Guarda las respuestas OMR por pregunta (batch)
     * Body: {
     *   "id_evaluacion": 123,
     *   "respuestas": [
     *     { "numero_pregunta": 1, "respuesta_marcada": "A", "confianza": 98.5 },
     *     { "numero_pregunta": 2, "respuesta_marcada": "B", "confianza": 95.2 },
     *     ...
     *   ]
     * }
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function guardarRespuestasOmr(Request $request)
    {
        $request->validate([
            'id_evaluacion' => 'required|exists:evaluaciones,id_evaluacion',
            'respuestas' => 'required|array|min:1',
            'respuestas.*.numero_pregunta' => 'required|integer|min:1',
            'respuestas.*.respuesta_marcada' => 'nullable|string|max:10',
            'respuestas.*.confianza' => 'nullable|numeric|min:0|max:100',
        ]);

        DB::beginTransaction();
        try {
            // Eliminar respuestas previas (si es re-evaluación)
            RespuestaOmr::where('evaluacion', $request->id_evaluacion)->delete();

            // Insertar nuevas respuestas
            $respuestas_guardadas = [];
            foreach ($request->respuestas as $resp) {
                $respuesta_omr = RespuestaOmr::create([
                    'evaluacion' => $request->id_evaluacion,
                    'numero_pregunta' => $resp['numero_pregunta'],
                    'respuesta_marcada' => $resp['respuesta_marcada'] ?? null,
                    'confianza' => $resp['confianza'] ?? null,
                ]);
                $respuestas_guardadas[] = $respuesta_omr->id_respuesta_omr;
            }

            DB::commit();

            return response()->json([
                'success' => true,
                'message' => 'Respuestas OMR guardadas exitosamente',
                'data' => [
                    'id_evaluacion' => $request->id_evaluacion,
                    'total_respuestas' => count($respuestas_guardadas),
                ]
            ], 201);

        } catch (\Exception $e) {
            DB::rollBack();
            return response()->json([
                'success' => false,
                'message' => 'Error al guardar respuestas OMR',
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT 6: GET /api/evaluaciones
     * Obtiene TODAS las evaluaciones con detalles completos
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function getAllEvaluaciones()
    {
        $evaluaciones = Evaluacion::with([
            'inscripcionRel.personaRel',
            'inscripcionRel.eventoRel',
            'resultadoRel'
        ])
        ->orderBy('fecha_evaluacion', 'desc')
        ->get()
        ->map(function ($eval) {
            $inscripcion = $eval->inscripcionRel;
            $persona = $inscripcion ? $inscripcion->personaRel : null;
            $evento = $inscripcion ? $inscripcion->eventoRel : null;
            $resultado = $eval->resultadoRel;

            // Construir rutas de archivos si existen
            $pdf_completo = null;
            $pdf_evidencia = null;
            
            if ($persona && $evento) {
                $dni = $persona->dni;
                $evento_nombre = str_replace(' ', '_', $evento->nombre);
                // Sanitizar nombre del evento como lo hace completo.py
                $evento_nombre = preg_replace('/[^a-zA-Z0-9\s_-]/', '_', $evento_nombre);
                $evento_nombre = str_replace(' ', '_', $evento_nombre);
                
                // Base path a public/resultados_omr
                $base_resultados = public_path("resultados_omr");
                
                // Buscar la carpeta que coincida con el nombre del evento (puede tener timestamp)
                $carpetas = glob("{$base_resultados}/{$evento_nombre}*", GLOB_ONLYDIR);
                
                if (!empty($carpetas)) {
                    // Usar la carpeta más reciente si hay varias
                    $carpeta_evento = end($carpetas);
                    $carpeta_nombre = basename($carpeta_evento);
                    
                    // PDF Completo (reporte_completo)
                    $pdf_completo_file = "{$carpeta_evento}/reporte_completo/{$dni}_hoja_completa.pdf";
                    if (file_exists($pdf_completo_file)) {
                        // URL pública directa
                        $pdf_completo = "/resultados_omr/{$carpeta_nombre}/reporte_completo/{$dni}_hoja_completa.pdf";
                    }
                    
                    // PDF Evidencia (evidencias)
                    $pdf_evidencia_file = "{$carpeta_evento}/evidencias/{$dni}_evidencia.pdf";
                    if (file_exists($pdf_evidencia_file)) {
                        $pdf_evidencia = "/resultados_omr/{$carpeta_nombre}/evidencias/{$dni}_evidencia.pdf";
                    }
                }
            }

            return [
                'id_evaluacion' => $eval->id_evaluacion,
                'fecha_evaluacion' => $eval->fecha_evaluacion,
                'tipo_examen' => $eval->tipo_examen,
                'estado' => $eval->estado,
                'observaciones' => $eval->observaciones,
                
                // Datos del evento
                'evento' => [
                    'id_evento' => $evento->id_evento ?? null,
                    'nombre' => $evento->nombre ?? 'N/A',
                    'fecha_evento' => $evento->fecha_evento ?? null,
                    'tipo_evento' => $evento->tipo_evento ?? null,
                ],
                
                // Datos del inscrito/persona
                'inscrito' => [
                    'id_inscripcion' => $inscripcion->id_inscripcion ?? null,
                    'dni' => $persona->dni ?? 'N/A',
                    'nombres_completos' => $persona 
                        ? trim("{$persona->nombres} {$persona->apPaterno} {$persona->apMaterno}")
                        : 'N/A',
                    'nombres' => $persona->nombres ?? 'N/A',
                    'apellido_paterno' => $persona->apPaterno ?? '',
                    'apellido_materno' => $persona->apMaterno ?? '',
                ],
                
                // Datos del resultado
                'resultado' => [
                    'puntaje' => $resultado->puntaje ?? 0,
                    'puntaje_maximo' => $resultado && $resultado->total_preguntas > 0 
                        ? $resultado->total_preguntas 
                        : 30,
                    'total_preguntas' => $resultado->total_preguntas ?? 30,
                    // Correctas = puntaje (cada pregunta vale 1 punto)
                    'correctas' => $resultado ? round($resultado->puntaje) : 0,
                    'aprobado' => $resultado ? $resultado->puntaje >= 20 : false,
                    'porcentaje' => $resultado && $resultado->total_preguntas > 0
                        ? round(($resultado->puntaje / $resultado->total_preguntas) * 100, 2)
                        : 0,
                    'fecha_calificacion' => $resultado->fecha_calificacion ?? null,
                ],
                
                // Rutas de archivos PDF
                'archivos' => [
                    'pdf_completo' => $pdf_completo,
                    'pdf_evidencia' => $pdf_evidencia,
                ],
            ];
        });

        return response()->json([
            'success' => true,
            'total' => $evaluaciones->count(),
            'data' => $evaluaciones
        ], 200);
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT 7: GET /api/evaluaciones/pdf/{id_evento}/{dni}/{tipo}
     * Descarga un PDF (completo o evidencia)
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function descargarPDF($id_evento, $dni, $tipo)
    {
        // Validar tipo
        if (!in_array($tipo, ['completo', 'evidencia'])) {
            return response()->json([
                'success' => false,
                'message' => 'Tipo de PDF inválido. Use "completo" o "evidencia".'
            ], 400);
        }

        // Buscar el evento
        $evento = Evento::find($id_evento);
        if (!$evento) {
            return response()->json([
                'success' => false,
                'message' => 'Evento no encontrado'
            ], 404);
        }

        // Construir nombre base del evento (sin timestamp)
        $evento_nombre = str_replace(' ', '_', $evento->nombre);
        $evento_nombre = preg_replace('/[^a-zA-Z0-9\s_-]/', '_', $evento_nombre);
        $evento_nombre = str_replace(' ', '_', $evento_nombre);
        $base_resultados = public_path("resultados_omr");
        
        // Buscar la carpeta que coincida con el nombre del evento (puede tener timestamp)
        $carpetas = glob("{$base_resultados}/{$evento_nombre}*", GLOB_ONLYDIR);
        
        if (empty($carpetas)) {
            return response()->json([
                'success' => false,
                'message' => 'No se encontró carpeta de resultados para este evento',
                'debug' => [
                    'evento_nombre' => $evento_nombre,
                    'base_path' => $base_resultados
                ]
            ], 404);
        }
        
        // Usar la carpeta más reciente si hay varias
        $carpeta_evento = end($carpetas);
        
        // Construir ruta del archivo
        if ($tipo === 'completo') {
            $file_path = "{$carpeta_evento}/reporte_completo/{$dni}_hoja_completa.pdf";
            $filename = "{$dni}_reporte_completo.pdf";
        } else {
            $file_path = "{$carpeta_evento}/evidencias/{$dni}_evidencia.pdf";
            $filename = "{$dni}_evidencia.pdf";
        }

        // Verificar que existe
        if (!file_exists($file_path)) {
            return response()->json([
                'success' => false,
                'message' => 'Archivo PDF no encontrado',
                'debug' => [
                    'carpeta_evento' => $carpeta_evento,
                    'file_path' => $file_path,
                    'tipo' => $tipo,
                    'dni' => $dni
                ]
            ], 404);
        }

        // Retornar el archivo
        return response()->file($file_path, [
            'Content-Type' => 'application/pdf',
            'Content-Disposition' => 'inline; filename="' . $filename . '"'
        ]);
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT LEGACY (mantener compatibilidad)
     * POST /api/omr/resultado
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function guardarResultadoOMR(Request $request)
    {
        $request->validate([
            'dni' => 'required|string|size:8',
            'evento' => 'required|integer',
            'puntaje' => 'required|numeric',
            'puntaje_maximo' => 'required|numeric',
            'porcentaje' => 'required|numeric',
            'pdf_path' => 'nullable|string'
        ]);

        // 1️⃣ Persona
        $persona = Persona::where('dni', $request->dni)->firstOrFail();

        // 2️⃣ Inscripción
        $inscripcion = Inscripcion::where('evento', $request->evento)
            ->where('persona', $persona->id_persona)
            ->firstOrFail();

        // 3️⃣ Evaluación (1 por inscripción)
        $evaluacion = Evaluacion::firstOrCreate(
            ['inscripcion' => $inscripcion->id_inscripcion],
            [
                'fecha_evaluacion' => now(),
                'tipo_examen' => 'regular',
                'estado' => 'valida'
            ]
        );

        // 4️⃣ Resultado
        Resultado::updateOrCreate(
            ['evaluacion' => $evaluacion->id_evaluacion],
            [
                'puntaje' => $request->puntaje,
                'total_preguntas' => 30,
                'aprobado' => $request->puntaje >= 20,
                'archivo_pdf' => $request->pdf_path ?? '',
                'fecha_calificacion' => now(),
            ]
        );

        return response()->json([
            'message' => 'Resultado OMR guardado correctamente'
        ], 201);
    }

    /**
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     * ENDPOINT: GET /api/evaluaciones/exportar/{id_evento?}
     * Exporta evaluaciones a Excel con diseño profesional
     * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     */
    public function exportarExcel($id_evento = null)
    {
        try {
            // Obtener evaluaciones usando los aliases Rel
            $query = Evaluacion::with([
                'inscripcionRel.personaRel',
                'inscripcionRel.eventoRel.tipoEvento',
                'resultadoRel',
                'respuestasOmr' // Cargar respuestas para calcular estadísticas
            ]);

            if ($id_evento) {
                $query->whereHas('inscripcionRel', function($q) use ($id_evento) {
                    $q->where('evento', $id_evento);
                });
            }

            $evaluaciones = $query->orderBy('created_at', 'desc')->get();

            // Obtener información del evento
            $evento = null;
            $tipoEvento = 'Todos';
            $nombreArchivo = 'evaluaciones_' . now()->format('Y-m-d_H-i-s') . '.xlsx';
            
            if ($id_evento) {
                $evento = Evento::with('tipoEvento')->find($id_evento);
                if ($evento) {
                    $tipoEvento = $evento->tipoEvento->nombre ?? 'General';
                    $nombreEvento = preg_replace('/[^A-Za-z0-9_\-]/', '_', $evento->nombre);
                    $nombreArchivo = $nombreEvento . '_' . now()->format('Y-m-d_H-i-s') . '.xlsx';
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
            
            // Crear Excel con diseño profesional usando PhpSpreadsheet
            $export = new EvaluacionesExcelExport($evaluaciones, $evento, $tipoEvento);
            $export->export($rutaArchivo);

            return response()->json([
                'success' => true,
                'message' => 'Excel generado exitosamente con diseño profesional',
                'data' => [
                    'nombre_archivo' => $nombreArchivo,
                    'ruta' => "excel/{$tipoEventoSlug}/{$nombreArchivo}",
                    'url' => url("excel/{$tipoEventoSlug}/{$nombreArchivo}"),
                    'tipo_evento' => $tipoEvento,
                    'evento' => $evento ? $evento->nombre : 'Todos los eventos',
                    'total_registros' => $evaluaciones->count(),
                ]
            ], 200);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al generar el Excel',
                'error' => $e->getMessage(),
                'trace' => config('app.debug') ? $e->getTraceAsString() : null,
            ], 500);
        }
    }
}
