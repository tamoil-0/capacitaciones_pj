<?php

namespace App\Http\Controllers;

use App\Models\Evento;
use App\Imports\EventPersonImport;
use Maatwebsite\Excel\Facades\Excel;
use Illuminate\Http\Request;

class EventoController extends Controller
{
    public function index($id_tipe)
    {
        $eventos = Evento::where('tipo_evento', $id_tipe)
            ->orderBy('id_evento', 'desc')
            ->get();

        if ($eventos->isEmpty()) {
            return response()->json(['message' => 'No se encontraron eventos para este tipo de evento'], 404);
        }

        return response()->json($eventos, 200);
    }

    // CREAR — fecha_evento por defecto: ahora (se puede cambiar)
    public function store(Request $request, $id_tipo_evento)
    {
        $request->merge(['tipo_evento' => $id_tipo_evento]);

        $data = $request->only(['nombre', 'fecha_evento', 'tipo_evento', 'estado']);
        if (empty($data['fecha_evento'])) {
            $data['fecha_evento'] = now()->format('Y-m-d H:i:s');
        }

        $evento = Evento::create($data);
        return response()->json($evento, 201);
    }

    // EDITAR — al pasar a Finalizado, fecha_fin por defecto: ahora
    public function update(Request $request, $id_evento)
    {
        $evento = Evento::find($id_evento);

        if (!$evento) {
            return response()->json(['message' => 'Evento no encontrado'], 404);
        }

        $data = $request->only(['nombre', 'fecha_evento', 'fecha_fin', 'estado']);
        $nuevoEstado = isset($data['estado']) ? (int) $data['estado'] : $evento->estado;

        if ($nuevoEstado === 1 && empty($data['fecha_fin'])) {
            $data['fecha_fin'] = now()->format('Y-m-d H:i:s');
        }
        if ($nuevoEstado === 0) {
            $data['fecha_fin'] = null;
        }

        $evento->update($data);
        return response()->json($evento, 200);
    }

    public function destroy(string $id_evento)
    {
        $evento = Evento::findOrFail($id_evento);
        $evento->delete();

        return response()->json(['message' => 'Evento eliminado correctamente']);
    }

    public function importar(Request $request, $id_tipo_evento)
    {
        $file = $request->file('file'); // o 'excel', depende del nombre del input
        Excel::import(new EventPersonImport($id_tipo_evento), $file);

        return response()->json(['message' => 'Importación completada correctamente']);
    }
}