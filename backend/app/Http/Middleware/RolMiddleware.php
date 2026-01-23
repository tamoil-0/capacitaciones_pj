<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class RolMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, ...$roles): Response
    {

        // Obtiene al usuario autenticado a través de Sanctum
        $usuario = $request->user();

        // Si no hay usuario autenticado o su tipo no está en los roles permitidos
        if (!$usuario || !in_array((string) $usuario->tipo_usuario, $roles)) {
            return response()->json(['message' => 'No autorizado'], 403);
        }

        return $next($request);
    }
    
}
