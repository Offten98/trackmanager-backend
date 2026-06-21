import customtkinter as ctk
from models.usuario import Usuario
from models.proyecto import Proyecto 
from models.archivo_audio import ArchivoAudio
from database.conexion import ConexionBD 

# 1. Configuración de apariencia
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

# 2. Ventana principal
ventana = ctk.CTk()
ventana.geometry("950x880") 
ventana.title("TrackManager Pro - Offten Studio")

titulo_principal = ctk.CTkLabel(ventana, text="🎵 Panel Maestro de Proyectos", font=("Arial", 24, "bold"), text_color="#FFFFFF")
titulo_principal.pack(pady=10) 

# --- PESTAÑAS ---
panel_pestanas = ctk.CTkTabview(ventana, width=880, height=750)
panel_pestanas.pack(pady=5, padx=20)

tab_usuarios = panel_pestanas.add("Usuarios")
tab_proyectos = panel_pestanas.add("Proyectos Musicales")
tab_audios = panel_pestanas.add("Archivos de Audio")

# ================================================================
# PESTAÑA 1: USUARIOS
# ================================================================
sub_usu = ctk.CTkLabel(tab_usuarios, text="Registro de Nuevo Usuario", font=("Arial", 16, "bold"), text_color="#FFFFFF")
sub_usu.pack(pady=5)

entrada_correo = ctk.CTkEntry(tab_usuarios, placeholder_text="Correo electrónico...", width=350)
entrada_correo.pack(pady=5)

opciones_cuenta = ctk.CTkOptionMenu(tab_usuarios, values=["Artista Independiente", "Mánager Premium"], width=350)
opciones_cuenta.pack(pady=5)

def guardar_usuario_gui():
    correo = entrada_correo.get()
    if not correo.strip(): return
    nuevo = Usuario(correo=correo, tipo_cuenta=opciones_cuenta.get())
    bd = ConexionBD(); con = bd.conectar()
    if con:
        nuevo.guardar_en_bd(con); bd.desconectar()
        etiqueta_estado_usu.configure(text=f"✅ Guardado: {correo}", text_color="#FFFFFF")
        entrada_correo.delete(0, 'end'); cargar_usuarios_gui()

boton_usu = ctk.CTkButton(tab_usuarios, text="Guardar Usuario", font=("Arial", 14, "bold"), text_color="#FFFFFF", command=guardar_usuario_gui)
boton_usu.pack(pady=10)
etiqueta_estado_usu = ctk.CTkLabel(tab_usuarios, text="", font=("Arial", 12))
etiqueta_estado_usu.pack()

caja_usuarios = ctk.CTkTextbox(tab_usuarios, width=700, height=150, font=("Courier New", 13), wrap="none")
caja_usuarios.pack(pady=10)

def cargar_usuarios_gui():
    caja_usuarios.configure(state="normal"); caja_usuarios.delete("1.0", "end")
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor(); cursor.execute("SELECT id_usuario, correo, tipo_cuenta FROM usuarios")
        regs = cursor.fetchall()
        caja_usuarios.insert("end", f"{'ID':<6} | {'CORREO ELECTRÓNICO':<35} | {'TIPO'}\n" + "-"*70 + "\n")
        for f in regs: caja_usuarios.insert("end", f"{f[0]:<6} | {f[1]:<35} | {f[2]}\n")
        bd.desconectar()
    caja_usuarios.configure(state="disabled")

# ================================================================
# PESTAÑA 2: PROYECTOS (Registro, Update, Lista y Búsqueda)
# ================================================================
sub_proy = ctk.CTkLabel(tab_proyectos, text="Crear Nueva Maqueta", font=("Arial", 16, "bold"), text_color="#FFFFFF")
sub_proy.pack(pady=5)

en_id_u = ctk.CTkEntry(tab_proyectos, placeholder_text="ID del Dueño...", width=350)
en_id_u.pack(pady=5)
en_tit = ctk.CTkEntry(tab_proyectos, placeholder_text="Título de la canción...", width=350)
en_tit.pack(pady=5)
op_gen = ctk.CTkOptionMenu(tab_proyectos, values=["Pop", "Dance-Pop", "Urbano", "Otro"], width=350)
op_gen.pack(pady=5)

def guardar_proyecto_gui():
    try:
        id_u = int(en_id_u.get()); tit = en_tit.get()
        if not tit.strip(): return
        nuevo = Proyecto(id_usuario=id_u, titulo_temp=tit, genero=op_gen.get())
        bd = ConexionBD(); con = bd.conectar()
        if con:
            nuevo.guardar_en_bd(con); bd.desconectar()
            etiqueta_estado_proy.configure(text=f"✅ Proyecto '{tit}' Creado", text_color="#FFFFFF")
            en_id_u.delete(0, 'end'); en_tit.delete(0, 'end'); cargar_proyectos_gui()
    except: pass

boton_proy = ctk.CTkButton(tab_proyectos, text="Guardar Proyecto", font=("Arial", 14, "bold"), text_color="#FFFFFF", command=guardar_proyecto_gui)
boton_proy.pack(pady=10)
etiqueta_estado_proy = ctk.CTkLabel(tab_proyectos, text="", font=("Arial", 12))
etiqueta_estado_proy.pack()

# --- NUEVA SECCIÓN: BARRA DE BÚSQUEDA Y FILTROS ---
marco_filtro = ctk.CTkFrame(tab_proyectos, fg_color="transparent")
marco_filtro.pack(pady=5)

ctk.CTkLabel(marco_filtro, text="🔍 Filtrar por Género:", font=("Arial", 12, "bold"), text_color="#FFFFFF").pack(side="left", padx=5)
op_filtro_gen = ctk.CTkOptionMenu(marco_filtro, values=["Todos", "Pop", "Dance-Pop", "Urbano", "Otro"], width=130)
op_filtro_gen.pack(side="left", padx=5)

def aplicar_filtro_gui():
    genero_seleccionado = op_filtro_gen.get()
    cargar_proyectos_gui(filtro_genero=genero_seleccionado)

boton_filtrar = ctk.CTkButton(marco_filtro, text="Filtrar", font=("Arial", 12, "bold"), text_color="#FFFFFF", width=80, command=aplicar_filtro_gui)
boton_filtrar.pack(side="left", padx=5)

caja_proyectos = ctk.CTkTextbox(tab_proyectos, width=700, height=130, font=("Courier New", 13), wrap="none")
caja_proyectos.pack(pady=5)

# Modificamos la función para que reciba el filtro (por defecto "Todos")
def cargar_proyectos_gui(filtro_genero="Todos"):
    caja_proyectos.configure(state="normal"); caja_proyectos.delete("1.0", "end")
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor()
        if filtro_genero == "Todos":
            sql = "SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo FROM proyectos p INNER JOIN usuarios u ON p.id_usuario = u.id_usuario"
            cursor.execute(sql)
        else:
            # Aquí aplicamos el poder de la cláusula WHERE
            sql = "SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo FROM proyectos p INNER JOIN usuarios u ON p.id_usuario = u.id_usuario WHERE p.genero = %s"
            cursor.execute(sql, (filtro_genero,))
            
        regs = cursor.fetchall()
        caja_proyectos.insert("end", f"{'ID':<4} | {'TÍTULO CANCIÓN':<20} | {'GÉNERO':<12} | {'FASE ACTUAL':<18} | {'DUEÑO'}\n" + "-"*85 + "\n")
        
        if not regs:
            caja_proyectos.insert("end", f"No hay canciones de género '{filtro_genero}' registradas.\n")
        else:
            for f in regs: caja_proyectos.insert("end", f"{f[0]:<4} | {f[1]:<20} | {f[2]:<12} | {f[3]:<18} | {f[4]}\n")
        bd.desconectar()
    caja_proyectos.configure(state="disabled")

# --- ACTUALIZAR FASE (UPDATE) ---
ctk.CTkLabel(tab_proyectos, text="🎚️ Actualizar Estado / Fase de la Canción", font=("Arial", 14, "bold"), text_color="#FFFFFF").pack(pady=5)

marco_fase = ctk.CTkFrame(tab_proyectos, fg_color="transparent")
marco_fase.pack(pady=2)

en_id_fase = ctk.CTkEntry(marco_fase, placeholder_text="ID Canción...", width=110)
en_id_fase.pack(side="left", padx=5)

op_fases_estudio = ctk.CTkOptionMenu(marco_fase, values=["Composición", "Grabación de Voces", "Mezcla", "Masterización", "Terminado"], width=180)
op_fases_estudio.pack(side="left", padx=5)

def actualizar_fase_gui():
    id_txt = en_id_fase.get()
    nueva_fase = op_fases_estudio.get()
    if not id_txt.strip(): return
    try: id_p = int(id_txt)
    except ValueError: return

    bd = ConexionBD(); con = bd.conectar()
    if con:
        proy_temp = Proyecto(id_usuario=0, titulo_temp="", genero="")
        exito = proy_temp.actualizar_fase(con, id_p, nueva_fase)
        bd.desconectar()
        if exito:
            etiqueta_estado_proy.configure(text=f"✨ ¡Canción ID {id_p} movida a '{nueva_fase}'!", text_color="#FFFFFF")
            en_id_fase.delete(0, 'end'); cargar_proyectos_gui(op_filtro_gen.get())

boton_fase = ctk.CTkButton(marco_fase, text="Actualizar Estado", font=("Arial", 12, "bold"), text_color="#FFFFFF", command=actualizar_fase_gui)
boton_fase.pack(side="left", padx=5)

# ================================================================
# PESTAÑA 3: AUDIOS 
# ================================================================
sub_aud = ctk.CTkLabel(tab_audios, text="Subir Nuevo Archivo de Audio", font=("Arial", 16, "bold"), text_color="#FFFFFF")
sub_aud.pack(pady=5)

en_id_p = ctk.CTkEntry(tab_audios, placeholder_text="ID del Proyecto...", width=350)
en_id_p.pack(pady=2)
op_cat = ctk.CTkOptionMenu(tab_audios, values=["Vocales", "Instrumental", "Master"], width=350)
op_cat.pack(pady=2)
op_for = ctk.CTkOptionMenu(tab_audios, values=["WAV", "MP3"], width=350)
op_for.pack(pady=2)
en_tam = ctk.CTkEntry(tab_audios, placeholder_text="Tamaño MB (ej. 12.5)...", width=350)
en_tam.pack(pady=2)
en_rut = ctk.CTkEntry(tab_audios, placeholder_text="Ruta del archivo...", width=350)
en_rut.pack(pady=2)

def guardar_audio_gui():
    try:
        id_p = int(en_id_p.get()); tam = float(en_tam.get()); rut = en_rut.get()
        nuevo = ArchivoAudio(id_proyecto=id_p, categoria=op_cat.get(), formato=op_for.get(), tamano_mb=tam, url_almacen=rut)
        bd = ConexionBD(); con = bd.conectar()
        if con:
            nuevo.guardar_en_bd(con); bd.desconectar()
            etiqueta_estado_aud.configure(text="✅ Audio Registrado", text_color="#FFFFFF")
            en_id_p.delete(0, 'end'); en_tam.delete(0, 'end'); en_rut.delete(0, 'end'); cargar_audios_gui()
    except: pass

boton_aud = ctk.CTkButton(tab_audios, text="Guardar Audio", font=("Arial", 14, "bold"), text_color="#FFFFFF", command=guardar_audio_gui)
boton_aud.pack(pady=10)
etiqueta_estado_aud = ctk.CTkLabel(tab_audios, text="", font=("Arial", 12))
etiqueta_estado_aud.pack()

ctk.CTkLabel(tab_audios, text="🔊 Archivos de Audio en el Sistema", font=("Arial", 14, "bold"), text_color="#FFFFFF").pack(pady=5)
caja_audios = ctk.CTkTextbox(tab_audios, width=700, height=130, font=("Courier New", 13), wrap="none")
caja_audios.pack(pady=5)

def cargar_audios_gui():
    caja_audios.configure(state="normal"); caja_audios.delete("1.0", "end")
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor()
        sql = "SELECT a.id_archivo, p.titulo_temp, a.categoria, a.formato, a.tamano_mb FROM archivos_audio a INNER JOIN proyectos p ON a.id_proyecto = p.id_proyecto"
        cursor.execute(sql)
        regs = cursor.fetchall()
        caja_audios.insert("end", f"{'ID':<4} | {'CANCIÓN':<20} | {'CATEGORÍA':<15} | {'FORMATO':<8} | {'TAMAÑO'}\n" + "-"*75 + "\n")
        for f in regs: caja_audios.insert("end", f"{f[0]:<4} | {f[1]:<20} | {f[2]:<15} | {f[3]:<8} | {f[4]} MB\n")
        bd.desconectar()
    caja_audios.configure(state="disabled")

# --- SECCIÓN DE ELIMINAR AUDIO ---
ctk.CTkLabel(tab_audios, text="🗑️ Eliminar Archivo de Audio", font=("Arial", 14, "bold"), text_color="#FFFFFF").pack(pady=10)

marco_eliminar = ctk.CTkFrame(tab_audios, fg_color="transparent")
marco_eliminar.pack(pady=5)

entrada_id_eliminar = ctk.CTkEntry(marco_eliminar, placeholder_text="ID a borrar...", width=150)
entrada_id_eliminar.pack(side="left", padx=10)

def eliminar_audio_gui():
    id_texto = entrada_id_eliminar.get()
    if not id_texto.strip(): return
    try: id_borrar = int(id_texto)
    except ValueError: return

    bd = ConexionBD(); con = bd.conectar()
    if con:
        audio_temp = ArchivoAudio(id_proyecto=0, categoria="", formato="", tamano_mb=0, url_almacen="")
        exito = audio_temp.eliminar_de_bd(con, id_borrar)
        bd.desconectar()
        if exito:
            etiqueta_estado_aud.configure(text=f"✅ Archivo con ID {id_borrar} eliminado.", text_color="#FFFFFF")
            entrada_id_eliminar.delete(0, 'end'); cargar_audios_gui()

boton_eliminar = ctk.CTkButton(marco_eliminar, text="Eliminar", font=("Arial", 12, "bold"), text_color="#FFFFFF", fg_color="#D9534F", hover_color="#C9302C", command=eliminar_audio_gui)
boton_eliminar.pack(side="left")

# Disparadores iniciales
ventana.after(100, cargar_usuarios_gui)
ventana.after(150, cargar_proyectos_gui) # Por defecto arranca en "Todos"
ventana.after(200, cargar_audios_gui)

if __name__ == "__main__":
    ventana.mainloop()