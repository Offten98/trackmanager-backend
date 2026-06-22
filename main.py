import customtkinter as ctk
from models.usuario import Usuario
from models.proyecto import Proyecto 
from models.archivo_audio import ArchivoAudio
from database.conexion import ConexionBD 

# 1. Ajuste de apariencia base
ctk.set_appearance_mode("dark")  

# 2. Ventana Principal - Fondo Obsidian Líquido Ultra Profundo
ventana = ctk.CTk()
ventana.geometry("980x880") 
ventana.title("TrackManager Pro - Offten Studio")
ventana.configure(fg_color="#060608") # Negro absoluto

# --- TIPOGRAFÍA Y2K RETRO-FUTURISTA ---
FUENTE_TITULO = ("Impact", 32)                           # Gruesa, agresiva y clásica de los 2000
FUENTE_SUBTITULO = ("Lucida Console", 14, "bold")        # Estilo terminal/cibernético
FUENTE_GENERAL = ("Verdana", 12)                         # La reina del internet temprano (Y2K)
FUENTE_BOTON = ("Verdana", 11, "bold")                   # Clara y fuerte
FUENTE_TABLA = ("Lucida Console", 12)                    # Textos de la base de datos estilo "Matrix"

# Encabezado Y2K Atrevido
titulo_principal = ctk.CTkLabel(
    ventana, 
    text="T R A C K M A N A G E R   P R O", 
    font=FUENTE_TITULO, 
    text_color="#FFFFFF"
)
titulo_principal.pack(pady=20) 

# --- SISTEMA DE PESTAÑAS ---
panel_pestanas = ctk.CTkTabview(
    ventana, 
    width=900, 
    height=760,
    fg_color="#0F0F16",                 
    border_width=0,
    border_color="#232330",             
    corner_radius=22,
    segmented_button_fg_color="#060608",       
    segmented_button_selected_color="#222232",  
    segmented_button_selected_hover_color="#2A2A3F", 
    segmented_button_unselected_hover_color="#14141F",
    text_color="#FFFFFF"
)
panel_pestanas.pack(pady=5, padx=20)

# Aplicar la fuente Y2K a los botones de las pestañas de forma correcta:
panel_pestanas._segmented_button.configure(font=FUENTE_BOTON)

tab_usuarios = panel_pestanas.add("Usuarios")
tab_proyectos = panel_pestanas.add("Proyectos Musicales")
tab_audios = panel_pestanas.add("Archivos de Audio")

# Estilos premium
def aplicar_estilo_boton_glass(boton, color_borde="#FFFFFF", color_hover="#1F1F2E"):
    boton.configure(
        fg_color="transparent",
        border_width=1,
        border_color=color_borde,
        text_color="#FFFFFF",
        hover_color=color_hover,
        corner_radius=16,
        font=FUENTE_BOTON
    )

def aplicar_estilo_input_glass(entrada):
    entrada.configure(
        fg_color="#0A0A0F",
        border_width=1,
        border_color="#2C2C3A",
        text_color="#FFFFFF",
        placeholder_text_color="#555566",
        corner_radius=14,
        font=FUENTE_GENERAL
    )

# ================================================================
# PESTAÑA 1: GESTIÓN DE USUARIOS
# ================================================================
sub_usu = ctk.CTkLabel(tab_usuarios, text="> REGISTRO DE NUEVO USUARIO_", font=FUENTE_SUBTITULO, text_color="#FFFFFF")
sub_usu.pack(pady=15)

entrada_correo = ctk.CTkEntry(tab_usuarios, placeholder_text="Correo electrónico...", width=380, height=42)
aplicar_estilo_input_glass(entrada_correo)
entrada_correo.pack(pady=8)

# [CORRECCIÓN DEL BUG DEL MENÚ DESPLEGABLE]
opciones_cuenta = ctk.CTkOptionMenu(
    tab_usuarios, 
    values=["Artista Independiente", "Mánager Premium"], 
    width=380, 
    height=42, 
    fg_color="#0A0A0F", 
    button_color="#1F1F2E", 
    button_hover_color="#2A2A3F", 
    text_color="#FFFFFF",
    font=FUENTE_GENERAL,
    corner_radius=14,
    anchor="center",                         # Centra el texto en el botón
    dropdown_fg_color="#0A0A0F",             # Estiliza la caja desplegable para que no quede blanca/fea
    dropdown_hover_color="#1F1F2E",
    dropdown_text_color="#FFFFFF",
    dropdown_font=FUENTE_GENERAL
)
opciones_cuenta.pack(pady=8)

def guardar_usuario_gui():
    correo = entrada_correo.get()
    if not correo.strip(): return
    nuevo = Usuario(correo=correo, tipo_cuenta=opciones_cuenta.get())
    bd = ConexionBD(); con = bd.conectar()
    if con:
        nuevo.guardar_en_bd(con); bd.desconectar()
        etiqueta_estado_usu.configure(text=f"[OK] Usuario indexado: {correo}", text_color="#FFFFFF")
        entrada_correo.delete(0, 'end'); cargar_usuarios_gui()

boton_usu = ctk.CTkButton(tab_usuarios, text="GUARDAR USUARIO", command=guardar_usuario_gui, height=42)
aplicar_estilo_boton_glass(boton_usu)
boton_usu.pack(pady=15)

etiqueta_estado_usu = ctk.CTkLabel(tab_usuarios, text="", font=FUENTE_GENERAL)
etiqueta_estado_usu.pack()

caja_usuarios = ctk.CTkTextbox(tab_usuarios, width=780, height=180, font=FUENTE_TABLA, wrap="none", fg_color="#060608", border_width=1, border_color="#1F1F2E", corner_radius=18)
caja_usuarios.pack(pady=15)

def cargar_usuarios_gui():
    caja_usuarios.configure(state="normal"); caja_usuarios.delete("1.0", "end")
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor(); cursor.execute("SELECT id_usuario, correo, tipo_cuenta FROM usuarios")
        regs = cursor.fetchall()
        caja_usuarios.insert("end", f"{'ID':<6} | {'CORREO ELECTRÓNICO':<40} | {'TIPO DE CUENTA'}\n" + "="*80 + "\n")
        for f in regs: caja_usuarios.insert("end", f"{f[0]:<6} | {f[1]:<40} | {f[2]}\n")
        bd.desconectar()
    caja_usuarios.configure(state="disabled")


# ================================================================
# PESTAÑA 2: PROYECTOS MUSICALES
# ================================================================
sub_proy = ctk.CTkLabel(tab_proyectos, text="> CREAR NUEVA MAQUETA MUSICAL_", font=FUENTE_SUBTITULO, text_color="#FFFFFF")
sub_proy.pack(pady=10)

en_id_u = ctk.CTkEntry(tab_proyectos, placeholder_text="ID del Dueño...", width=380, height=40)
aplicar_estilo_input_glass(en_id_u); en_id_u.pack(pady=6)

en_tit = ctk.CTkEntry(tab_proyectos, placeholder_text="Título de la canción...", width=380, height=40)
aplicar_estilo_input_glass(en_tit); en_tit.pack(pady=6)

# [MENÚ CORREGIDO]
op_gen = ctk.CTkOptionMenu(
    tab_proyectos, values=["Pop", "Dance-Pop", "Urbano", "Otro"], 
    width=380, height=40, fg_color="#0A0A0F", button_color="#1F1F2E", font=FUENTE_GENERAL, corner_radius=14,
    anchor="center", dropdown_fg_color="#0A0A0F", dropdown_hover_color="#1F1F2E", dropdown_text_color="#FFFFFF", dropdown_font=FUENTE_GENERAL
)
op_gen.pack(pady=6)

def guardar_proyecto_gui():
    try:
        id_u = int(en_id_u.get()); tit = en_tit.get()
        if not tit.strip(): return
        nuevo = Proyecto(id_usuario=id_u, titulo_temp=tit, genero=op_gen.get())
        bd = ConexionBD(); con = bd.conectar()
        if con:
            nuevo.guardar_en_bd(con); bd.desconectar()
            etiqueta_estado_proy.configure(text=f"[OK] Proyecto '{tit}' creado exitosamente.", text_color="#FFFFFF")
            en_id_u.delete(0, 'end'); en_tit.delete(0, 'end'); cargar_proyectos_gui()
    except: pass

boton_proy = ctk.CTkButton(tab_proyectos, text="CREAR PROYECTO", command=guardar_proyecto_gui, height=42)
aplicar_estilo_boton_glass(boton_proy); boton_proy.pack(pady=12)

etiqueta_estado_proy = ctk.CTkLabel(tab_proyectos, text="", font=FUENTE_GENERAL)
etiqueta_estado_proy.pack()

# Buscador
marco_filtro = ctk.CTkFrame(tab_proyectos, fg_color="transparent")
marco_filtro.pack(pady=8)

ctk.CTkLabel(marco_filtro, text="Filtrar por Género:", font=FUENTE_GENERAL, text_color="#FFFFFF").pack(side="left", padx=8)

# [MENÚ CORREGIDO]
op_filtro_gen = ctk.CTkOptionMenu(
    marco_filtro, values=["Todos", "Pop", "Dance-Pop", "Urbano", "Otro"], 
    width=140, fg_color="#0A0A0F", button_color="#1F1F2E", font=FUENTE_GENERAL, corner_radius=12,
    anchor="center", dropdown_fg_color="#0A0A0F", dropdown_hover_color="#1F1F2E", dropdown_text_color="#FFFFFF", dropdown_font=FUENTE_GENERAL
)
op_filtro_gen.pack(side="left", padx=5)

def aplicar_filtro_gui():
    cargar_proyectos_gui(filtro_genero=op_filtro_gen.get())

boton_filtrar = ctk.CTkButton(marco_filtro, text="FILTRAR", command=aplicar_filtro_gui, width=90, height=32)
aplicar_estilo_boton_glass(boton_filtrar); boton_filtrar.pack(side="left", padx=8)

caja_proyectos = ctk.CTkTextbox(tab_proyectos, width=780, height=150, font=FUENTE_TABLA, wrap="none", fg_color="#060608", border_width=1, border_color="#1F1F2E", corner_radius=18)
caja_proyectos.pack(pady=8)

def cargar_proyectos_gui(filtro_genero="Todos"):
    caja_proyectos.configure(state="normal"); caja_proyectos.delete("1.0", "end")
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor()
        if filtro_genero == "Todos":
            sql = "SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo FROM proyectos p INNER JOIN usuarios u ON p.id_usuario = u.id_usuario"
            cursor.execute(sql)
        else:
            sql = "SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo FROM proyectos p INNER JOIN usuarios u ON p.id_usuario = u.id_usuario WHERE p.genero = %s"
            cursor.execute(sql, (filtro_genero,))
            
        regs = cursor.fetchall()
        caja_proyectos.insert("end", f"{'ID':<4} | {'TÍTULO CANCIÓN':<22} | {'GÉNERO':<12} | {'FASE ACTUAL':<20} | {'DUEÑO'}\n" + "="*85 + "\n")
        if not regs:
            caja_proyectos.insert("end", f"No se encontraron proyectos del género '{filtro_genero}'.\n")
        else:
            for f in regs: caja_proyectos.insert("end", f"{f[0]:<4} | {f[1]:<22} | {f[2]:<12} | {f[3]:<20} | {f[4]}\n")
        bd.desconectar()
    caja_proyectos.configure(state="disabled")

# Panel de Actualización
marco_fase = ctk.CTkFrame(tab_proyectos, fg_color="#13131F", border_width=1, border_color="#2A2A3F", corner_radius=18, height=75)
marco_fase.pack(pady=15, padx=20, fill="x")

ctk.CTkLabel(marco_fase, text="[ CONTROL DE FASE ]", font=FUENTE_SUBTITULO, text_color="#FFFFFF").pack(side="left", padx=15, pady=18)
en_id_fase = ctk.CTkEntry(marco_fase, placeholder_text="ID...", width=70, height=36)
aplicar_estilo_input_glass(en_id_fase); en_id_fase.pack(side="left", padx=10)

# [MENÚ CORREGIDO]
op_fases_estudio = ctk.CTkOptionMenu(
    marco_fase, values=["Composición", "Grabación de Voces", "Mezcla", "Masterización", "Terminado"], 
    width=180, height=36, fg_color="#060608", button_color="#1F1F2E", font=FUENTE_GENERAL, corner_radius=12,
    anchor="center", dropdown_fg_color="#0A0A0F", dropdown_hover_color="#1F1F2E", dropdown_text_color="#FFFFFF", dropdown_font=FUENTE_GENERAL
)
op_fases_estudio.pack(side="left", padx=10)

def actualizar_fase_gui():
    id_txt = en_id_fase.get()
    if not id_txt.strip(): return
    try: id_p = int(id_txt)
    except ValueError: return
    bd = ConexionBD(); con = bd.conectar()
    if con:
        proy_temp = Proyecto(id_usuario=0, titulo_temp="", genero="")
        exito = proy_temp.actualizar_fase(con, id_p, op_fases_estudio.get())
        bd.desconectar()
        if exito:
            en_id_fase.delete(0, 'end'); cargar_proyectos_gui(op_filtro_gen.get())

boton_fase = ctk.CTkButton(marco_fase, text="ACTUALIZAR ESTADO", command=actualizar_fase_gui, height=36, width=150)
aplicar_estilo_boton_glass(boton_fase); boton_fase.pack(side="left", padx=15)


# ================================================================
# PESTAÑA 3: ARCHIVOS DE AUDIO
# ================================================================
sub_aud = ctk.CTkLabel(tab_audios, text="> SUBIR NUEVO STEM / AUDIO AL SISTEMA_", font=FUENTE_SUBTITULO, text_color="#FFFFFF")
sub_aud.pack(pady=10)

en_id_p = ctk.CTkEntry(tab_audios, placeholder_text="ID del Proyecto...", width=380, height=38)
aplicar_estilo_input_glass(en_id_p); en_id_p.pack(pady=4)

# [MENÚ CORREGIDO]
op_cat = ctk.CTkOptionMenu(
    tab_audios, values=["Vocales", "Instrumental", "Master"], 
    width=380, height=38, fg_color="#0A0A0F", button_color="#1F1F2E", font=FUENTE_GENERAL, corner_radius=14,
    anchor="center", dropdown_fg_color="#0A0A0F", dropdown_hover_color="#1F1F2E", dropdown_text_color="#FFFFFF", dropdown_font=FUENTE_GENERAL
)
op_cat.pack(pady=4)

# [MENÚ CORREGIDO]
op_for = ctk.CTkOptionMenu(
    tab_audios, values=["WAV", "MP3"], 
    width=380, height=38, fg_color="#0A0A0F", button_color="#1F1F2E", font=FUENTE_GENERAL, corner_radius=14,
    anchor="center", dropdown_fg_color="#0A0A0F", dropdown_hover_color="#1F1F2E", dropdown_text_color="#FFFFFF", dropdown_font=FUENTE_GENERAL
)
op_for.pack(pady=4)

en_tam = ctk.CTkEntry(tab_audios, placeholder_text="Tamaño MB (ej. 12.5)...", width=380, height=38)
aplicar_estilo_input_glass(en_tam); en_tam.pack(pady=4)

en_rut = ctk.CTkEntry(tab_audios, placeholder_text="Ruta lógica de almacenamiento...", width=380, height=38)
aplicar_estilo_input_glass(en_rut); en_rut.pack(pady=4)

def guardar_audio_gui():
    try:
        id_p = int(en_id_p.get()); tam = float(en_tam.get()); rut = en_rut.get()
        nuevo = ArchivoAudio(id_proyecto=id_p, categoria=op_cat.get(), formato=op_for.get(), tamano_mb=tam, url_almacen=rut)
        bd = ConexionBD(); con = bd.conectar()
        if con:
            nuevo.guardar_en_bd(con); bd.desconectar()
            etiqueta_estado_aud.configure(text="[OK] Audio indexado correctamente.", text_color="#FFFFFF")
            en_id_p.delete(0, 'end'); en_tam.delete(0, 'end'); en_rut.delete(0, 'end'); cargar_audios_gui()
    except: pass

boton_aud = ctk.CTkButton(tab_audios, text="REGISTRAR AUDIO", command=guardar_audio_gui, height=42)
aplicar_estilo_boton_glass(boton_aud); boton_aud.pack(pady=10)

etiqueta_estado_aud = ctk.CTkLabel(tab_audios, text="", font=FUENTE_GENERAL)
etiqueta_estado_aud.pack()

caja_audios = ctk.CTkTextbox(tab_audios, width=780, height=140, font=FUENTE_TABLA, wrap="none", fg_color="#060608", border_width=1, border_color="#1F1F2E", corner_radius=18)
caja_audios.pack(pady=5)

def cargar_audios_gui():
    caja_audios.configure(state="normal"); caja_audios.delete("1.0", "end")
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor()
        sql = "SELECT a.id_archivo, p.titulo_temp, a.categoria, a.formato, a.tamano_mb FROM archivos_audio a INNER JOIN proyectos p ON a.id_proyecto = p.id_proyecto"
        cursor.execute(sql)
        regs = cursor.fetchall()
        caja_audios.insert("end", f"{'ID':<4} | {'CANCIÓN COMPOSICIÓN':<24} | {'CATEGORÍA':<15} | {'FORMATO':<8} | {'TAMAÑO'}\n" + "="*75 + "\n")
        for f in regs: caja_audios.insert("end", f"{f[0]:<4} | {f[1]:<24} | {f[2]:<15} | {f[3]:<8} | {f[4]} MB\n")
        bd.desconectar()
    caja_audios.configure(state="disabled")

# Destrucción Sutil
marco_eliminar = ctk.CTkFrame(tab_audios, fg_color="#130B0B", border_width=1, border_color="#D9534F", corner_radius=18, height=65)
marco_eliminar.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(marco_eliminar, text="[ REMOVER ARCHIVO DEL SISTEMA ]", font=FUENTE_SUBTITULO, text_color="#FFFFFF").pack(side="left", padx=15, pady=18)
entrada_id_eliminar = ctk.CTkEntry(marco_eliminar, placeholder_text="ID...", width=80, height=36)
aplicar_estilo_input_glass(entrada_id_eliminar); entrada_id_eliminar.pack(side="left", padx=10)

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
            entrada_id_eliminar.delete(0, 'end'); cargar_audios_gui()

boton_eliminar = ctk.CTkButton(marco_eliminar, text="ELIMINAR REGISTRO", command=eliminar_audio_gui, height=36, width=150, fg_color="transparent", border_width=1, border_color="#D9534F", text_color="#FFFFFF", hover_color="#2D1212", corner_radius=12, font=FUENTE_BOTON)
boton_eliminar.pack(side="left", padx=15)

# Hilos de renderizado inicial automático
ventana.after(100, cargar_usuarios_gui)
ventana.after(150, cargar_proyectos_gui)
ventana.after(200, cargar_audios_gui)

if __name__ == "__main__":
    ventana.mainloop()