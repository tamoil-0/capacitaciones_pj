<?php

namespace App\Http\Controllers;

use App\Models\Usuario;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UsuarioController extends Controller
{
    public function index()
    {
        $usuarios = Usuario::where('tipo_usuario', '!=', 1)->get();
        return response()->json($usuarios);
    }

    public function store(Request $request)
    {
        $request->validate([
            'nombres_apellidos' => 'required|string|max:255',
            'nickname'          => 'required|string|max:50',
            'contrasena'        => 'required|string|min:6',
            'tipo_usuario'      => 'required|integer',
            'asignado'          => 'required|integer',
            'habilitado'        => 'required|boolean',
        ]);

        $usuario = Usuario::create([
            'nombres_apellidos' => $request->nombres_apellidos,
            'nickname'          => $request->nickname,
            'contrasena'        => Hash::make($request->contrasena),
            'tipo_usuario'      => $request->tipo_usuario,
            'asignado'          => $request->asignado,
            'habilitado'        => $request->habilitado,
        ]);

        return response()->json($usuario, 201);
    }

    public function show(string $id_usuario)
    {
        $usuario = Usuario::findOrFail($id_usuario);
        return response()->json($usuario);
    } //use Illuminate\Validation\Rule;

    public function update(Request $request, string $id_usuario)
    {
        $usuario = Usuario::findOrFail($id_usuario);

        $request->validate([
            'nombres_apellidos' => 'sometimes|string|max:255',
            'nickname'          => 'sometimes|string|max:50',
            'tipo_usuario'      => 'required|integer',
            'habilitado'        => 'required|boolean', 
        ]);

        $usuario->update($request->all());

        return response()->json($usuario);
    }

    public function destroy(string $id_usuario)
    {
        $user = Usuario::findOrFail($id_usuario);
        $user->delete();

        return response()->json(['message' => 'Usuario eliminado correctamente']);
    }

    public function restablecerPassword(Request $request, string $id_usuario)
    {
        $request->validate([
            'contraseña_nueva' => 'required|string',
        ]);

        $user = Usuario::findOrFail($id_usuario);

        // Guardar nueva contraseña
        $user->contrasena = Hash::make($request->contraseña_nueva);
        $user->save();

        return response()->json(['message' => 'Contraseña restablecida correctamente']);
    }

    public function cambiarPassword(Request $request, string $id)
    {
        $request->validate([
            'contraseña_actual' => 'required|string',
            'contraseña_nueva' => 'required|string|min:6|confirmed', // requiere campo contraseña_nueva_confirmation
        ]);

        $user = Usuario::findOrFail($id);

        // Verificar contraseña actual
        if (!Hash::check($request->contraseña_actual, $user->contrasena)) {
            return response()->json(['error' => 'La contraseña actual no es correcta'], 400);
        }

        // Guardar nueva contraseña
        $user->contrasena = Hash::make($request->contraseña_nueva);
        $user->save();

        return response()->json(['message' => 'Contraseña actualizada correctamente']);
    }
}
