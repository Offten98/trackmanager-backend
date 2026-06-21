# TrackManager Pro - Offten Studio 🎵

TrackManager Pro es una aplicación de escritorio desarrollada en Python orientada a la gestión y control de flujos de producción musical, maquetas y almacenamiento de archivos de audio (*stems*, pistas vocales, instrumentales y másters). El sistema integra una interfaz gráfica de usuario moderna con una arquitectura de base de datos relacional robusta.

## 🚀 Características Principales

- **Gestión de Usuarios:** Registro estructurado de cuentas de artistas y mánagers con almacenamiento seguro en base de datos.
- **Control de Proyectos Musicales:** Creación y seguimiento de maquetas musicales enfocadas en géneros como Pop, Dance-Pop y Urbano, vinculadas directamente a su respectivo dueño mediante llaves foráneas.
- **Administración de Archivos de Audio:** Registro técnico de pistas de audio asociadas a cada proyecto, detallando formato (WAV, MP3), tamaño en megabytes y rutas lógicas de almacenamiento.
- **Consultas Relacionales Integradas:** Renderizado de datos cruzados en tiempo real mediante operaciones `INNER JOIN` ejecutadas directamente hacia componentes visuales independientes.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje de Programación:** Python 3
- **Interfaz Gráfica (Front-End):** CustomTkinter (Modo oscuro de alta fidelidad)
- **Base de Datos (Back-End):** MySQL (Gestionado mediante XAMPP y phpMyAdmin)
- **Control de Versiones:** Git y GitHub

## 📊 Arquitectura del Sistema (Modelo Relacional)

El backend se rige bajo las reglas de integridad referencial de una base de datos MySQL, compuesta por tres entidades principales:
1. **usuarios:** Entidad primaria que identifica a los miembros del sistema.
2. **proyectos:** Almacena los títulos provisionales de las canciones, géneros y fases del proceso, conectada a la tabla de usuarios mediante la llave foránea `id_usuario`.
3. **archivos_audio:** Registra las pistas específicas de audio, vinculada de forma estricta a la tabla de proyectos mediante la llave foránea `id_proyecto`.

## 📦 Instalación y Despliegue Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TuUsuario/trackmanager-backend.git](https://github.com/TuUsuario/trackmanager-backend.git)
   cd trackmanager-backend