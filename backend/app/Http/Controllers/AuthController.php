<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Models\Usuario;
use App\Models\Opcion;

use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $credentials = $request->validate([
            'nickname' => 'required|string',
            'password' => 'required|string',
        ]);

        $usuario = Usuario::where('nickname', $credentials['nickname'])->first();
        if (!$usuario) {
            return response()->json(['error' => 'Usuario no encontrado'], 404);
        }
        if ($usuario->habilitado == 0) {
            return response()->json(['error' => 'Tu usuario no está habilitado'], 403);
        }
        if (!$usuario || !Hash::check($credentials['password'], $usuario->contrasena)) {
            return response()->json(['message' => 'Contrasena inválidas'], 401);
        }

        $token = $usuario->createToken('gcpj_token')->plainTextToken;

        $opciones = Opcion::where('id_tipu', $usuario->tipo_usuario)->get();

        // 👉 Aquí aplicas la regla
        if ($usuario->tipo_usuario > 1) {
            foreach ($opciones as $op) {
                if (strtolower($op->nombre) === "eventos") {
                    // Concatenar /asignado
                    $op->ruta = rtrim($op->ruta, '/') . '/' . $usuario->asignado;
                }
            }
        }

        return response()->json([
            'message' => 'Inicio de Sesion Exitoso',
            'token' => $token,
            'usuario' => [
                'id_usuario'        => $usuario->id_usuario,
                'nombres_apellidos' => $usuario->nombres_apellidos,
                'nickname'          => $usuario->nickname,
                'tipo_usuario'      => $usuario->tipo_usuario,
            ],
            'opciones' => $opciones,
        ]);
    }
}
