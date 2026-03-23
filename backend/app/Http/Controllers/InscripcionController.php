<?php

namespace App\Http\Controllers;

use App\Models\Persona;
use App\Models\Inscripcion;
use Illuminate\Http\Request;

use App\Imports\PersonasImport;
use Maatwebsite\Excel\Facades\Excel;

class InscripcionController extends Controller
{
public function index($id_evento)
{
    $inscripciones = Inscripcion::with('persona')
        ->where('evento', $id_evento)
        ->withCount([
            'registros as entradas' => function ($q) {
                $q->where('tipo', 'Entrada');
            },
            'registros as salidas' => function ($q) {
                $q->where('tipo', 'Salida');
            },
        ])
        ->get()
        ->map(function ($inscripcion) {
            // Obtener última entrada y última salida
            $ultimaEntrada = $inscripcion->registros()
                ->where('tipo', 'Entrada')
                ->latest('created_at')
                ->first();
            
            $ultimaSalida = $inscripcion->registros()
                ->where('tipo', 'Salida')
                ->latest('created_at')
                ->first();
            
            // Agregar las horas al objeto
            $inscripcion->ultima_entrada = $ultimaEntrada 
                ? $ultimaEntrada->created_at->format('H:i:s') 
                : null;
            
            $inscripcion->ultima_salida = $ultimaSalida 
                ? $ultimaSalida->created_at->format('H:i:s') 
                : null;
            
            return $inscripcion;
        });

    return response()->json($inscripciones);
}


    // CREAR
    public function store(Request $request, $id_evento)
    {
        // Validamos los datos mínimos
        $validated = $request->validate([
            'dni'       => 'required|string|max:8',
            'nombres'   => 'required|string|max:100',
            'apPaterno' => 'required|string|max:100',
            'apMaterno' => 'required|string|max:100',
        ]);

        // Verificar si existe la persona
        $persona = Persona::where('dni', $validated['dni'])->first();

        // Si no existe, crear una nueva
        if (!$persona) {
            $persona = Persona::create([
                'dni'        => $validated['dni'],
                'nombres'    => $validated['nombres'],
                'apPaterno'  => $validated['apPaterno'],
                'apMaterno'  => $validated['apMaterno'],
            ]);
        }

        // Crear la inscripción
        $inscripcion = Inscripcion::create([
            'evento' => $id_evento,
            'persona'  => $persona->id_persona,
        ]);

        return response()->json($inscripcion, 201);
    }

    public function importar(Request $request, $id_evento)
    {
        $request->validate([
            'file' => 'required|mimes:xlsx,csv,xls'
        ]);

        Excel::import(new PersonasImport($id_evento), $request->file('file'));

        return response()->json(['message' => 'Importación realizada con éxito']);
    }
    /**
    * Asistencia
    */
    public function update($id_evento, $dni)
    {
        // Buscar usuario por DNI
        $persona = Persona::where('dni', $dni)->first();

        if (!$persona) {
            return response()->json([
                'message' => 'Usuario no encontrado'
            ], 404);
        }

        // Buscar inscrito según id_evento y usuario
        $inscrito = Inscripcion::where('evento', $id_evento)
                                ->where('persona', $persona->id_persona)
                                ->first();

        if (!$inscrito) {
            return response()->json([
                'message' => 'Inscripción no encontrada'
            ], 404);
        }

        // Cambiar estado de 0 a 1
        $inscrito->asistio = 1;
        $inscrito->save();

        return response()->json([
            'message' => 'Asistencia tomada correctamente'
        ]);
    }


    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id_evento)
    {
        $inscripcion = Inscripcion::find($id_evento);

        if (!$inscripcion) {
            return response()->json(['message' => 'Inscripcion no encontrado'], 404);
        }

        $inscripcion->delete();

        return response()->json(['message' => 'Inscripcion eliminado'], 200);
    }
    
    
}
