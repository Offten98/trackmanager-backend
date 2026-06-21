-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-06-2026 a las 19:03:42
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `trackmanager_pro`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_audio`
--

CREATE TABLE `archivos_audio` (
  `id_archivo` int(11) NOT NULL,
  `id_proyecto` int(11) NOT NULL,
  `categoria` varchar(50) NOT NULL,
  `formato` varchar(10) NOT NULL,
  `tamano_mb` decimal(5,2) DEFAULT NULL,
  `url_almacen` varchar(255) NOT NULL,
  `fecha_subida` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `archivos_audio`
--

INSERT INTO `archivos_audio` (`id_archivo`, `id_proyecto`, `categoria`, `formato`, `tamano_mb`, `url_almacen`, `fecha_subida`) VALUES
(1, 1, 'Vocales', 'WAV', 12.50, '/audios/voces.wav', '2026-06-21 01:50:50'),
(2, 1, 'Vocales', 'WAV', 15.50, '/voces/toma1.wav', '2026-06-21 16:37:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyectos`
--

CREATE TABLE `proyectos` (
  `id_proyecto` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `titulo_temp` varchar(100) NOT NULL,
  `genero` varchar(50) DEFAULT NULL,
  `fase_actual` varchar(50) DEFAULT 'Composición',
  `notas_prod` text DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proyectos`
--

INSERT INTO `proyectos` (`id_proyecto`, `id_usuario`, `titulo_temp`, `genero`, `fase_actual`, `notas_prod`, `fecha_creacion`) VALUES
(1, 4, 'HolaMundo', 'Urbano', 'Composición', '', '2026-06-21 01:36:18'),
(2, 6, 'Tu', 'Pop', 'Composición', '', '2026-06-21 16:19:04');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `tipo_cuenta` varchar(50) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `correo`, `tipo_cuenta`, `fecha_registro`) VALUES
(1, 'productor@estudio.com', 'Mánager Premium', '2026-06-21 01:07:18'),
(4, 'dj_prueba@musica.com', 'Artista Independiente', '2026-06-21 01:20:25'),
(6, 'nuevo_artista@estudio.com', 'Artista Independiente', '2026-06-21 16:09:08'),
(7, 'charlixcx@apple.com', 'Artista Independiente', '2026-06-21 16:22:35');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `archivos_audio`
--
ALTER TABLE `archivos_audio`
  ADD PRIMARY KEY (`id_archivo`),
  ADD KEY `id_proyecto` (`id_proyecto`);

--
-- Indices de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD PRIMARY KEY (`id_proyecto`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `archivos_audio`
--
ALTER TABLE `archivos_audio`
  MODIFY `id_archivo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  MODIFY `id_proyecto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `archivos_audio`
--
ALTER TABLE `archivos_audio`
  ADD CONSTRAINT `archivos_audio_ibfk_1` FOREIGN KEY (`id_proyecto`) REFERENCES `proyectos` (`id_proyecto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD CONSTRAINT `proyectos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
