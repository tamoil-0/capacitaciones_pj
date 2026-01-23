<?php

namespace App\Http\Controllers;

use App\Models\Persona;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;

class PersonaController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return response()->json(Persona::all(), 200);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $request->validate([
            'dni' => 'required|string|max:8|unique:personas,dni',
            'nombres' => 'required|string|max:255',
            'apPaterno' => 'required|string|max:255',
            'apMaterno' => 'required|string|max:255',
        ]);

        $persona = Persona::create([
            'dni' => $request->dni,
            'nombres' => $request->nombres,
            'apPaterno' => $request->apPaterno,
            'apMaterno' => $request->apMaterno,
        ]);

        return response()->json($persona, 201);
        
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {/*
        $user = User::findOrFail($id);
        return response()->json($user);*/
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id_persona)
    {
        $persona = Persona::findOrFail($id_persona);

        $request->validate([
            'nombres'      => 'sometimes|string|max:255',
            'apPaterno'    => 'sometimes|string|max:255',
            'apMaterno'    => 'sometimes|string|max:255',
            'dni'          => [
                'sometimes',
                'string',
                'max:8',
                Rule::unique('personas', 'dni')->ignore($persona->id_persona, 'id_persona'),
            ], 
        ]);

        $persona->update($request->all());

        return response()->json($persona);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id_persona)
    {
        $persona = Persona::findOrFail($id_persona);
        $persona->delete();

        return response()->json(['message' => 'Persona eliminado correctamente']);
    }
}


