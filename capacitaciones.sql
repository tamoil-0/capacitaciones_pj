-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-01-2026 a las 07:01:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `capacitaciones`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evaluaciones`
--

CREATE TABLE `evaluaciones` (
  `id_evaluacion` bigint(20) UNSIGNED NOT NULL,
  `inscripcion` bigint(20) UNSIGNED NOT NULL,
  `fecha_evaluacion` datetime NOT NULL,
  `tipo_examen` varchar(50) NOT NULL DEFAULT 'regular',
  `estado` enum('valida','invalida','anulada') NOT NULL DEFAULT 'valida',
  `observaciones` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `evaluaciones`
--

INSERT INTO `evaluaciones` (`id_evaluacion`, `inscripcion`, `fecha_evaluacion`, `tipo_examen`, `estado`, `observaciones`, `created_at`, `updated_at`) VALUES
(1, 3, '2026-01-05 03:43:16', 'regular', 'valida', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(2, 2, '2026-01-05 03:43:17', 'regular', 'valida', NULL, '2026-01-05 08:43:17', '2026-01-05 08:43:17'),
(3, 3, '2026-01-05 04:06:31', 'regular', 'valida', NULL, '2026-01-05 09:06:31', '2026-01-05 09:06:31'),
(4, 2, '2026-01-05 04:06:33', 'regular', 'valida', NULL, '2026-01-05 09:06:33', '2026-01-05 09:06:33'),
(5, 3, '2026-01-05 04:33:47', 'regular', 'valida', NULL, '2026-01-05 09:33:47', '2026-01-05 09:33:47'),
(6, 2, '2026-01-05 04:33:49', 'regular', 'valida', NULL, '2026-01-05 09:33:49', '2026-01-05 09:33:49'),
(7, 3, '2026-01-05 04:34:39', 'regular', 'valida', NULL, '2026-01-05 09:34:39', '2026-01-05 09:34:39'),
(8, 2, '2026-01-05 04:34:41', 'regular', 'valida', NULL, '2026-01-05 09:34:41', '2026-01-05 09:34:41'),
(9, 3, '2026-01-05 04:39:34', 'regular', 'valida', NULL, '2026-01-05 09:39:34', '2026-01-05 09:39:34'),
(10, 2, '2026-01-05 04:39:36', 'regular', 'valida', NULL, '2026-01-05 09:39:36', '2026-01-05 09:39:36'),
(11, 3, '2026-01-05 04:49:46', 'regular', 'valida', NULL, '2026-01-05 09:49:46', '2026-01-05 09:49:46'),
(12, 2, '2026-01-05 04:49:48', 'regular', 'valida', NULL, '2026-01-05 09:49:48', '2026-01-05 09:49:48'),
(13, 3, '2026-01-05 05:07:14', 'regular', 'valida', NULL, '2026-01-05 10:07:14', '2026-01-05 10:07:14'),
(14, 2, '2026-01-05 05:07:16', 'regular', 'valida', NULL, '2026-01-05 10:07:16', '2026-01-05 10:07:16'),
(15, 3, '2026-01-05 05:14:21', 'regular', 'valida', NULL, '2026-01-05 10:14:21', '2026-01-05 10:14:21'),
(16, 2, '2026-01-05 05:14:23', 'regular', 'valida', NULL, '2026-01-05 10:14:23', '2026-01-05 10:14:23'),
(17, 3, '2026-01-05 05:24:04', 'regular', 'valida', NULL, '2026-01-05 10:24:04', '2026-01-05 10:24:04'),
(18, 2, '2026-01-05 05:24:06', 'regular', 'valida', NULL, '2026-01-05 10:24:06', '2026-01-05 10:24:06'),
(19, 50, '2026-01-05 05:30:03', 'regular', 'valida', NULL, '2026-01-05 10:30:03', '2026-01-05 10:30:03'),
(20, 49, '2026-01-05 05:30:05', 'regular', 'valida', NULL, '2026-01-05 10:30:05', '2026-01-05 10:30:05'),
(21, 50, '2026-01-05 05:47:15', 'regular', 'valida', NULL, '2026-01-05 10:47:15', '2026-01-05 10:47:15'),
(22, 49, '2026-01-05 05:47:17', 'regular', 'valida', NULL, '2026-01-05 10:47:17', '2026-01-05 10:47:17');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id_evento` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `fecha_evento` datetime DEFAULT NULL,
  `tipo_evento` bigint(20) UNSIGNED NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `eventos`
--

INSERT INTO `eventos` (`id_evento`, `nombre`, `fecha_evento`, `tipo_evento`, `estado`, `fecha_creacion`) VALUES
(1, 'EXAMEN PRUEBA', '2025-12-22 12:14:00', 2, 1, '2025-12-22 16:14:57'),
(2, 'even1', '2025-12-22 12:17:00', 3, 1, '2025-12-22 16:17:44'),
(3, 'CAPACITACI├ôN DERECHO PENAL', '2026-01-15 10:00:00', 1, 1, '2026-01-05 04:22:39'),
(4, 'CURSO DERECHO LABORAL', '2026-01-20 14:00:00', 2, 1, '2026-01-05 04:22:39'),
(5, 'CAPACITACI├ôN DERECHO PENAL', '2026-01-15 10:00:00', 1, 1, '2026-01-05 04:24:08'),
(6, 'CURSO DERECHO LABORAL', '2026-01-20 14:00:00', 2, 1, '2026-01-05 04:24:08'),
(7, 'EVALUACI├ôN INTERMEDIA', '2026-01-15 09:00:00', 2, 1, '2026-01-05 04:27:19'),
(8, 'EXAMEN FINAL TRIMESTRE', '2026-01-25 14:30:00', 2, 1, '2026-01-05 04:27:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `id_inscripcion` bigint(20) UNSIGNED NOT NULL,
  `evento` bigint(20) UNSIGNED NOT NULL,
  `persona` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `inscripciones`
--

INSERT INTO `inscripciones` (`id_inscripcion`, `evento`, `persona`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2025-12-22 16:35:23', NULL),
(2, 1, 2, '2026-01-05 03:31:04', '2026-01-05 03:31:04'),
(3, 1, 3, '2026-01-05 03:31:04', '2026-01-05 03:31:04'),
(8, 3, 7, NULL, NULL),
(10, 4, 8, NULL, NULL),
(11, 4, 9, NULL, NULL),
(12, 4, 10, NULL, NULL),
(16, 5, 6, NULL, NULL),
(17, 5, 7, NULL, NULL),
(19, 6, 8, NULL, NULL),
(20, 6, 9, NULL, NULL),
(21, 6, 10, NULL, NULL),
(22, 1, 18, NULL, NULL),
(23, 1, 19, NULL, NULL),
(25, 7, 20, NULL, NULL),
(26, 7, 21, NULL, NULL),
(27, 7, 2, NULL, NULL),
(28, 7, 3, NULL, NULL),
(32, 8, 22, NULL, NULL),
(33, 8, 23, NULL, NULL),
(34, 8, 24, NULL, NULL),
(35, 8, 25, NULL, NULL),
(39, 2, 2, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(40, 2, 3, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(41, 3, 2, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(42, 3, 3, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(43, 4, 2, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(44, 4, 3, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(45, 5, 2, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(46, 5, 3, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(47, 6, 2, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(48, 6, 3, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(49, 8, 2, '2026-01-05 10:29:34', '2026-01-05 10:29:34'),
(50, 8, 3, '2026-01-05 10:29:34', '2026-01-05 10:29:34');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '2019_12_14_000001_create_personal_access_tokens_table', 1),
(2, '2025_09_23_040647_create_usuarios_table', 1),
(3, '2025_09_23_134858_create_eventos_table', 1),
(4, '2025_09_23_135911_create_personas_table', 1),
(5, '2025_09_23_140501_create_inscripciones_table', 1),
(6, '2026_01_04_000001_create_evaluaciones_table', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `opciones`
--

CREATE TABLE `opciones` (
  `id_op` bigint(20) UNSIGNED NOT NULL,
  `id_tipu` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `icono` varchar(100) NOT NULL,
  `ruta` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `opciones`
--

INSERT INTO `opciones` (`id_op`, `id_tipu`, `nombre`, `icono`, `ruta`, `created_at`, `updated_at`) VALUES
(1, 1, 'Eventos', 'mdi-certificate', '/tipos_eventos', NULL, NULL),
(2, 1, 'Usuarios', 'mdi-account-tie', '/usuarios', NULL, NULL),
(3, 1, 'Personas', 'mdi-account', '/personas', NULL, NULL),
(4, 2, 'Eventos', 'mdi-certificate', '/eventos/', NULL, NULL),
(5, 2, 'Usuarios', 'mdi-account', '/usuarios', NULL, NULL),
(6, 3, 'Eventos', 'mdi-certificate', '/eventos/', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal_access_tokens`
--

CREATE TABLE `personal_access_tokens` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `tokenable_type` varchar(255) NOT NULL,
  `tokenable_id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `token` varchar(64) NOT NULL,
  `abilities` text DEFAULT NULL,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `personal_access_tokens`
--

INSERT INTO `personal_access_tokens` (`id`, `tokenable_type`, `tokenable_id`, `name`, `token`, `abilities`, `last_used_at`, `expires_at`, `created_at`, `updated_at`) VALUES
(1, 'App\\Models\\Usuario', 1, 'gcpj_token', '8757738c5c93d6b0590f55a159db802593f98c07130cf75e6613e3315e0ac32a', '[\"*\"]', '2025-12-22 21:24:53', NULL, '2025-12-22 11:59:40', '2025-12-22 21:24:53'),
(2, 'App\\Models\\Usuario', 1, 'gcpj_token', 'b05ae4c9dd0305690c00f30b18b9367ab278eeaabf5af13cd2559d1f0807cc21', '[\"*\"]', '2025-12-22 21:36:40', NULL, '2025-12-22 21:30:34', '2025-12-22 21:36:40'),
(3, 'App\\Models\\Usuario', 1, 'gcpj_token', '308ab6617f7995646aefa30f21a7e347f0caf03e8b93a452f7d4ee199d658d46', '[\"*\"]', '2026-01-05 09:56:14', NULL, '2026-01-05 07:53:37', '2026-01-05 09:56:14'),
(4, 'App\\Models\\Usuario', 1, 'gcpj_token', '36a05c0b6a2291a075aecabdd23b2a41b3e7ece02d39fdce0362413b9a8dda47', '[\"*\"]', '2026-01-05 10:57:32', NULL, '2026-01-05 09:45:46', '2026-01-05 10:57:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personas`
--

CREATE TABLE `personas` (
  `id_persona` bigint(20) UNSIGNED NOT NULL,
  `dni` varchar(8) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apPaterno` varchar(100) NOT NULL,
  `apMaterno` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `personas`
--

INSERT INTO `personas` (`id_persona`, `dni`, `nombres`, `apPaterno`, `apMaterno`, `created_at`, `updated_at`) VALUES
(1, '71170816', 'Wilber', 'Mamani', 'Quispe', '2025-12-22 21:16:56', '2025-12-22 21:16:56'),
(2, '70025674', 'Wilber', 'Mamani', 'Mamani', '2026-01-05 03:31:04', '2026-01-05 03:31:04'),
(3, '72170816', 'Wilber', 'Mamani', 'Quispe', '2026-01-05 03:31:04', '2026-01-05 03:31:04'),
(6, '45782193', 'Roberto', 'Quispe', 'Mamani', NULL, NULL),
(7, '48965123', 'Carmen', 'Flores', 'Valencia', NULL, NULL),
(8, '52341678', 'Miguel ├üngel', 'Torres', 'Gutierrez', NULL, NULL),
(9, '55678234', 'Ana Mar├¡a', 'Vargas', 'Soto', NULL, NULL),
(10, '58912345', 'Luis Fernando', 'Huam├ín', 'Cruz', NULL, NULL),
(18, '40246548', 'Maribel Soledad', 'Quina', 'Jhuncacni', NULL, NULL),
(19, '41867217', 'Elanio', 'Artica', 'Alejo', NULL, NULL),
(20, '45678912', 'Carlos Eduardo', 'Mendoza', 'R├¡os', NULL, NULL),
(21, '48521367', 'Ana Mar├¡a', 'Torres', 'Vega', NULL, NULL),
(22, '52147896', 'Jorge Luis', 'Flores', 'Castillo', NULL, NULL),
(23, '55896321', 'Patricia Elena', 'Ram├¡rez', 'Soto', NULL, NULL),
(24, '58741236', 'Miguel ├üngel', 'Vargas', 'Cruz', NULL, NULL),
(25, '62589741', 'Rosa Linda', 'Guti├®rrez', 'Paredes', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros`
--

CREATE TABLE `registros` (
  `id_registro` bigint(20) UNSIGNED NOT NULL,
  `inscripcion` bigint(20) UNSIGNED NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `registros`
--

INSERT INTO `registros` (`id_registro`, `inscripcion`, `tipo`, `created_at`, `updated_at`) VALUES
(1, 1, 'Entrada', '2025-12-22 21:36:36', '2025-12-22 21:36:36');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_omr`
--

CREATE TABLE `respuestas_omr` (
  `id_respuesta_omr` bigint(20) UNSIGNED NOT NULL,
  `evaluacion` bigint(20) UNSIGNED NOT NULL,
  `numero_pregunta` int(11) NOT NULL,
  `respuesta_marcada` varchar(10) DEFAULT NULL,
  `confianza` decimal(5,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `respuestas_omr`
--

INSERT INTO `respuestas_omr` (`id_respuesta_omr`, `evaluacion`, `numero_pregunta`, `respuesta_marcada`, `confianza`, `created_at`, `updated_at`) VALUES
(1, 1, 1, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(2, 1, 2, 'D', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(3, 1, 3, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(4, 1, 4, 'B', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(5, 1, 5, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(6, 1, 6, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(7, 1, 7, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(8, 1, 8, 'B', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(9, 1, 9, 'D', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(10, 1, 10, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(11, 1, 11, 'D', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(12, 1, 12, 'D', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(13, 1, 13, 'B', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(14, 1, 14, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(15, 1, 15, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(16, 1, 16, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(17, 1, 17, 'B', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(18, 1, 18, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(19, 1, 19, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(20, 1, 20, 'B', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(21, 1, 21, 'C', NULL, '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(660, 22, 30, 'C', NULL, '2026-01-05 10:47:17', '2026-01-05 10:47:17');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados`
--

CREATE TABLE `resultados` (
  `id_resultado` bigint(20) UNSIGNED NOT NULL,
  `evaluacion` bigint(20) UNSIGNED NOT NULL,
  `puntaje` decimal(5,2) NOT NULL,
  `total_preguntas` int(11) NOT NULL DEFAULT 30,
  `aprobado` tinyint(1) NOT NULL DEFAULT 0,
  `archivo_pdf` varchar(500) DEFAULT NULL,
  `fecha_calificacion` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `resultados`
--

INSERT INTO `resultados` (`id_resultado`, `evaluacion`, `puntaje`, `total_preguntas`, `aprobado`, `archivo_pdf`, `fecha_calificacion`, `created_at`, `updated_at`) VALUES
(1, 1, 100.00, 30, 1, 'resultados_omr\\72170816_2.pdf', '2026-01-05 03:43:16', '2026-01-05 08:43:16', '2026-01-05 08:43:16'),
(2, 2, 100.00, 30, 1, 'resultados_omr\\70025674_2.pdf', '2026-01-05 03:43:17', '2026-01-05 08:43:17', '2026-01-05 08:43:17'),
(3, 3, 100.00, 30, 1, 'resultados_omr\\72170816_3.pdf', '2026-01-05 04:06:31', '2026-01-05 09:06:31', '2026-01-05 09:06:31'),
(4, 4, 100.00, 30, 1, 'resultados_omr\\70025674_3.pdf', '2026-01-05 04:06:33', '2026-01-05 09:06:33', '2026-01-05 09:06:33'),
(5, 5, 100.00, 30, 1, 'resultados_omr\\72170816_5.pdf', '2026-01-05 04:33:47', '2026-01-05 09:33:47', '2026-01-05 09:33:47'),
(6, 6, 100.00, 30, 1, 'resultados_omr\\70025674_5.pdf', '2026-01-05 04:33:49', '2026-01-05 09:33:49', '2026-01-05 09:33:49'),
(7, 7, 100.00, 30, 1, 'resultados_omr\\72170816_6.pdf', '2026-01-05 04:34:40', '2026-01-05 09:34:40', '2026-01-05 09:34:40'),
(8, 8, 100.00, 30, 1, 'resultados_omr\\70025674_6.pdf', '2026-01-05 04:34:42', '2026-01-05 09:34:42', '2026-01-05 09:34:42'),
(9, 9, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260104_233931\\evidencias_reporte\\72170816_evidencia.pdf', '2026-01-05 04:39:34', '2026-01-05 09:39:34', '2026-01-05 09:39:34'),
(10, 10, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260104_233931\\evidencias_reporte\\70025674_evidencia.pdf', '2026-01-05 04:39:36', '2026-01-05 09:39:36', '2026-01-05 09:39:36'),
(11, 11, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260104_234942\\evidencias_reporte\\72170816_evidencia.pdf', '2026-01-05 04:49:46', '2026-01-05 09:49:46', '2026-01-05 09:49:46'),
(12, 12, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260104_234942\\evidencias_reporte\\70025674_evidencia.pdf', '2026-01-05 04:49:48', '2026-01-05 09:49:48', '2026-01-05 09:49:48'),
(13, 13, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260105_000712\\evidencias_reporte\\72170816_evidencia.pdf', '2026-01-05 05:07:14', '2026-01-05 10:07:14', '2026-01-05 10:07:14'),
(14, 14, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260105_000712\\evidencias_reporte\\70025674_evidencia.pdf', '2026-01-05 05:07:17', '2026-01-05 10:07:17', '2026-01-05 10:07:17'),
(15, 15, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260105_001419\\evidencias_reporte\\72170816_evidencia.pdf', '2026-01-05 05:14:21', '2026-01-05 10:14:21', '2026-01-05 10:14:21'),
(16, 16, 100.00, 30, 1, 'resultados_omr\\EXAMEN_PRUEBA_20260105_001419\\evidencias_reporte\\70025674_evidencia.pdf', '2026-01-05 05:14:23', '2026-01-05 10:14:23', '2026-01-05 10:14:23'),
(17, 17, 8.00, 30, 0, 'resultados_omr\\EXAMEN_PRUEBA_20260105_002402\\evidencias_reporte\\72170816_evidencia.pdf', '2026-01-05 05:24:04', '2026-01-05 10:24:04', '2026-01-05 10:24:04'),
(18, 18, 10.00, 30, 0, 'resultados_omr\\EXAMEN_PRUEBA_20260105_002402\\evidencias_reporte\\70025674_evidencia.pdf', '2026-01-05 05:24:06', '2026-01-05 10:24:06', '2026-01-05 10:24:06'),
(19, 19, 8.00, 30, 0, 'resultados_omr\\EXAMEN_FINAL_TRIMESTRE_20260105_003001\\evidencias_reporte\\72170816_evidencia.pdf', '2026-01-05 05:30:03', '2026-01-05 10:30:03', '2026-01-05 10:30:03'),
(20, 20, 10.00, 30, 0, 'resultados_omr\\EXAMEN_FINAL_TRIMESTRE_20260105_003001\\evidencias_reporte\\70025674_evidencia.pdf', '2026-01-05 05:30:06', '2026-01-05 10:30:06', '2026-01-05 10:30:06'),
(21, 21, 8.00, 30, 0, 'resultados_omr\\EXAMEN_FINAL_TRIMESTRE_20260105_004712\\evidencias_reporte\\72170816_evidencia.pdf', '2026-01-05 05:47:15', '2026-01-05 10:47:15', '2026-01-05 10:47:15'),
(22, 22, 10.00, 30, 0, 'resultados_omr\\EXAMEN_FINAL_TRIMESTRE_20260105_004712\\evidencias_reporte\\70025674_evidencia.pdf', '2026-01-05 05:47:17', '2026-01-05 10:47:17', '2026-01-05 10:47:17');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_eventos`
--

CREATE TABLE `tipo_eventos` (
  `id_tipe` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `tipo_eventos`
--

INSERT INTO `tipo_eventos` (`id_tipe`, `nombre`) VALUES
(1, 'Convocatoria'),
(2, 'Cursos'),
(3, 'Otros');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_usuarios`
--

CREATE TABLE `tipo_usuarios` (
  `id_tipu` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `tipo_usuarios`
--

INSERT INTO `tipo_usuarios` (`id_tipu`, `nombre`, `created_at`, `updated_at`) VALUES
(1, 'administrador', NULL, NULL),
(2, 'organizador', NULL, NULL),
(3, 'ayudante', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` bigint(20) UNSIGNED NOT NULL,
  `nombres_apellidos` varchar(255) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `tipo_usuario` bigint(20) UNSIGNED NOT NULL,
  `asignado` bigint(20) UNSIGNED DEFAULT NULL,
  `habilitado` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--  
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombres_apellidos`, `nickname`, `contrasena`, `tipo_usuario`, `asignado`, `habilitado`, `created_at`, `updated_at`) VALUES
(1, 'Corte Superior de Justicia', 'pjudicial', '$2y$10$kk/eH8G8XEz3iNaqe237/ORcOdASQaANeFfs1iB.Q9ObLsFA1VS9C', 1, NULL, 1, NULL, NULL),
(2, 'Paola Karin Zirena Asencio', 'pzirenaa', '$2y$10$kk/eH8G8XEz3iNaqe237/ORcOdASQaANeFfs1iB.Q9ObLsFA1VS9C', 2, 1, 1, NULL, NULL),
(3, 'Elard Abdon Medina Aguilar', 'emedinaa', '$2y$10$kk/eH8G8XEz3iNaqe237/ORcOdASQaANeFfs1iB.Q9ObLsFA1VS9C', 3, 1, 1, NULL, NULL),
(4, 'Rolando Lazaro Quispe Garcia', 'rquispeg', '$2y$10$kk/eH8G8XEz3iNaqe237/ORcOdASQaANeFfs1iB.Q9ObLsFA1VS9C', 3, 1, 1, NULL, NULL),
(5, 'Gabriel Octavio Pacsi Mena', 'gpacsim', '$2y$10$kk/eH8G8XEz3iNaqe237/ORcOdASQaANeFfs1iB.Q9ObLsFA1VS9C', 3, 1, 1, NULL, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  ADD PRIMARY KEY (`id_evaluacion`),
  ADD KEY `evaluaciones_inscripcion_foreign` (`inscripcion`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id_evento`),
  ADD KEY `eventos_tipo_evento_foreign` (`tipo_evento`);

--
-- Indices de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD PRIMARY KEY (`id_inscripcion`),
  ADD KEY `inscripciones_evento_foreign` (`evento`),
  ADD KEY `inscripciones_persona_foreign` (`persona`);

--
-- Indices de la tabla `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `opciones`
--
ALTER TABLE `opciones`
  ADD PRIMARY KEY (`id_op`),
  ADD KEY `opciones_id_tipu_foreign` (`id_tipu`);

--
-- Indices de la tabla `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  ADD KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`);

--
-- Indices de la tabla `personas`
--
ALTER TABLE `personas`
  ADD PRIMARY KEY (`id_persona`),
  ADD UNIQUE KEY `personas_dni_unique` (`dni`);

--
-- Indices de la tabla `registros`
--
ALTER TABLE `registros`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `registros_inscripcion_foreign` (`inscripcion`);

--
-- Indices de la tabla `respuestas_omr`
--
ALTER TABLE `respuestas_omr`
  ADD PRIMARY KEY (`id_respuesta_omr`),
  ADD UNIQUE KEY `respuestas_omr_evaluacion_numero_pregunta_unique` (`evaluacion`,`numero_pregunta`);

--
-- Indices de la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD PRIMARY KEY (`id_resultado`),
  ADD KEY `resultados_evaluacion_foreign` (`evaluacion`);

--
-- Indices de la tabla `tipo_eventos`
--
ALTER TABLE `tipo_eventos`
  ADD PRIMARY KEY (`id_tipe`);

--
-- Indices de la tabla `tipo_usuarios`
--
ALTER TABLE `tipo_usuarios`
  ADD PRIMARY KEY (`id_tipu`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuarios_nickname_unique` (`nickname`),
  ADD KEY `usuarios_tipo_usuario_foreign` (`tipo_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  MODIFY `id_evaluacion` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id_evento` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `id_inscripcion` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `opciones`
--
ALTER TABLE `opciones`
  MODIFY `id_op` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `personas`
--
ALTER TABLE `personas`
  MODIFY `id_persona` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `registros`
--
ALTER TABLE `registros`
  MODIFY `id_registro` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `respuestas_omr`
--
ALTER TABLE `respuestas_omr`
  MODIFY `id_respuesta_omr` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=661;

--
-- AUTO_INCREMENT de la tabla `resultados`
--
ALTER TABLE `resultados`
  MODIFY `id_resultado` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `tipo_eventos`
--
ALTER TABLE `tipo_eventos`
  MODIFY `id_tipe` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tipo_usuarios`
--
ALTER TABLE `tipo_usuarios`
  MODIFY `id_tipu` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  ADD CONSTRAINT `evaluaciones_inscripcion_foreign` FOREIGN KEY (`inscripcion`) REFERENCES `inscripciones` (`id_inscripcion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD CONSTRAINT `eventos_tipo_evento_foreign` FOREIGN KEY (`tipo_evento`) REFERENCES `tipo_eventos` (`id_tipe`) ON DELETE CASCADE;

--
-- Filtros para la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD CONSTRAINT `inscripciones_evento_foreign` FOREIGN KEY (`evento`) REFERENCES `eventos` (`id_evento`) ON DELETE CASCADE,
  ADD CONSTRAINT `inscripciones_persona_foreign` FOREIGN KEY (`persona`) REFERENCES `personas` (`id_persona`) ON DELETE CASCADE;

--
-- Filtros para la tabla `opciones`
--
ALTER TABLE `opciones`
  ADD CONSTRAINT `opciones_id_tipu_foreign` FOREIGN KEY (`id_tipu`) REFERENCES `tipo_usuarios` (`id_tipu`) ON DELETE CASCADE;

--
-- Filtros para la tabla `registros`
--
ALTER TABLE `registros`
  ADD CONSTRAINT `registros_inscripcion_foreign` FOREIGN KEY (`inscripcion`) REFERENCES `inscripciones` (`id_inscripcion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `respuestas_omr`
--
ALTER TABLE `respuestas_omr`
  ADD CONSTRAINT `respuestas_omr_evaluacion_foreign` FOREIGN KEY (`evaluacion`) REFERENCES `evaluaciones` (`id_evaluacion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD CONSTRAINT `resultados_evaluacion_foreign` FOREIGN KEY (`evaluacion`) REFERENCES `evaluaciones` (`id_evaluacion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_tipo_usuario_foreign` FOREIGN KEY (`tipo_usuario`) REFERENCES `tipo_usuarios` (`id_tipu`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
