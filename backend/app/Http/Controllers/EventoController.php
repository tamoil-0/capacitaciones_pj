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

    // CREAR
    public function store(Request $request, $id_tipo_evento)
    {
        $request->merge([
            'tipo_evento' => $id_tipo_evento
        ]);

        $evento = Evento::create($request->all());

        return response()->json($evento, 201);
    }

    // EDITAR
    public function update(Request $request, $id_evento)
    {
        $evento = Evento::find($id_evento);

        if (!$evento) {
            return response()->json(['message' => 'Evento no encontrado'], 404);
        }

        $evento->update($request->all());

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