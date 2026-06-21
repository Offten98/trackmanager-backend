from models.usuario import Usuario
from models.proyecto import Proyecto
from models.archivo_audio import ArchivoAudio # <-- Importamos nuestra última pieza
from database.conexion import ConexionBD 

def mostrar_menu():
    print("\n" + "="*40)
    print(" 🎵 TRACKMANAGER PRO - PANEL MAESTRO 🎵")
    print("="*40)
    print("[1] Registrar nuevo usuario")
    print("[2] Ver usuarios registrados")
    print("[3] Crear nuevo proyecto musical")
    print("[4] Ver proyectos activos")
    print("[5] Subir archivo de audio a proyecto")
    print("[6] Salir del sistema")
    print("="*40)

def main():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1 al 6): ")

        if opcion == '1':
            print("\n--- NUEVO REGISTRO ---")
            correo_input = input("Ingresa el correo del usuario: ")
            print("Tipos de cuenta: [A] Artista Independiente | [M] Mánager Premium")
            tipo_input = input("Elige el tipo (A/M): ").upper()
            
            tipo_cuenta = "Artista Independiente" if tipo_input == 'A' else "Mánager Premium"

            nuevo_cliente = Usuario(correo=correo_input, tipo_cuenta=tipo_cuenta)
            bd = ConexionBD()
            conexion_activa = bd.conectar()
            if conexion_activa:
                nuevo_cliente.guardar_en_bd(conexion_activa)
                bd.desconectar()

        elif opcion == '2':
            bd = ConexionBD()
            conexion_activa = bd.conectar()
            if conexion_activa:
                Usuario.mostrar_todos(conexion_activa)
                bd.desconectar()

        elif opcion == '3':
            print("\n--- NUEVO PROYECTO MUSICAL ---")
            try:
                id_dueno = int(input("Ingresa el ID del usuario dueño del proyecto: "))
                titulo = input("Ingresa el título provisional de la canción: ")
                genero = input("Ingresa el género musical (ej. Pop, Urbano, Rock): ")

                nuevo_proyecto = Proyecto(id_usuario=id_dueno, titulo_temp=titulo, genero=genero)

                bd = ConexionBD()
                conexion_activa = bd.conectar()
                if conexion_activa:
                    nuevo_proyecto.guardar_en_bd(conexion_activa)
                    bd.desconectar()
            except ValueError:
                print("❌ Error: El ID del usuario debe ser un número entero.")

        elif opcion == '4':
            bd = ConexionBD()
            conexion_activa = bd.conectar()
            if conexion_activa:
                Proyecto.mostrar_todos(conexion_activa)
                bd.desconectar()

        elif opcion == '5':
            print("\n--- SUBIR ARCHIVO DE AUDIO ---")
            try:
                # Pedimos el ID del Proyecto (el número 1 que viste en tu captura anterior)
                id_proj = int(input("Ingresa el ID del Proyecto al que pertenece el audio: "))
                categoria = input("Categoría (ej. Instrumental, Vocales, Master): ")
                formato = input("Formato (ej. WAV, MP3): ").upper()
                tamano = float(input("Tamaño en MB (ej. 45.5): "))
                url = input("Ruta de almacenamiento (ej. /servidor/voces_toma1.wav): ")

                nuevo_audio = ArchivoAudio(id_proyecto=id_proj, categoria=categoria, formato=formato, tamano_mb=tamano, url_almacen=url)

                bd = ConexionBD()
                conexion_activa = bd.conectar()
                if conexion_activa:
                    nuevo_audio.guardar_en_bd(conexion_activa)
                    bd.desconectar()
            except ValueError:
                print("❌ Error: Verifica que el ID sea entero y el tamaño sea un número (usa punto para decimales).")

        elif opcion == '6':
            print("\n🔌 Cerrando TrackManager Pro... ¡Éxito total en tu desarrollo!")
            break  
        
        else:
            print("\n❌ Opción no válida. Por favor, escribe un número del 1 al 6.")

if __name__ == "__main__":
    main()