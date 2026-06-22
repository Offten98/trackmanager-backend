# 🎛️ TrackManager Pro - SaaS Music Studio

TrackManager Pro es una plataforma integral en la nube diseñada para resolver la desorganización en el flujo de trabajo de productores musicales y artistas independientes. Desarrollada con un enfoque especial en la gestión de stems para producciones de géneros contemporáneos (Pop, Urbano, Dance-Pop), permite centralizar maquetas, controlar el almacenamiento de archivos de audio y gestionar el progreso de las composiciones en un entorno completamente privado.

## 🚀 Características Principales

* **Arquitectura Multi-tenancy (Aislamiento de Datos):** Sistema multiusuario donde cada cuenta opera en un entorno privado. Los proyectos y audios están estrictamente vinculados al ID de sesión del usuario logeado mediante consultas SQL seguras.
* **Procesamiento de Archivos Binarios:** Motor de subida de archivos `.wav` y `.mp3` con validación backend, renombramiento seguro (`secure_filename`) y cálculo automático de peso (MB) y formato.
* **Gestión Eficiente de Recursos:** Sistema de borrado físico optimizado. Al eliminar un registro de la base de datos, el servidor ejecuta una limpieza automática en el disco duro para evitar archivos huérfanos.
* **Seguridad y Validación Estricta:** 
  * Encriptación de contraseñas (*Hashing*) mediante `werkzeug.security`.
  * Validación de dominios de correo electrónico en tiempo real mediante resolución DNS (`email-validator`) para evitar cuentas falsas.
  * Prevención de errores de claves foráneas con *rollbacks* de archivos en caso de excepciones.
* **Interfaz "Liquid Glass":** Diseño frontend limpio, inmersivo y responsivo, con un panel de métricas dinámico calculado en tiempo real desde el backend.

## 🛠️ Stack Tecnológico

* **Backend:** Python 3, Flask.
* **Base de Datos:** MySQL (Relacional).
* **Frontend:** HTML5, CSS3 puro (Liquid Glass UI).
* **Entorno:** Entorno virtual aislado (`.venv`).

## ⚙️ Instalación y Ejecución Local

1. Clona este repositorio:
```bash
   git clone [https://github.com/tu-usuario/trackmanager-pro.git](https://github.com/tu-usuario/trackmanager-pro.git)