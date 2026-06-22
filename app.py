from flask import Flask, render_template, request, redirect, url_for
from database.conexion import ConexionBD
from models.usuario import Usuario
from models.proyecto import Proyecto
from models.archivo_audio import ArchivoAudio

app = Flask(__name__)

# ==========================================
# RUTA 1: GESTIÓN DE USUARIOS
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def inicio():
    bd = ConexionBD()
    con = bd.conectar()
    
    if request.method == 'POST' and con:
        correo_form = request.form.get('correo')
        tipo_form = request.form.get('tipo_cuenta')
        if correo_form and tipo_form:
            nuevo_usuario = Usuario(correo=correo_form, tipo_cuenta=tipo_form)
            nuevo_usuario.guardar_en_bd(con)
        bd.desconectar()
        return redirect(url_for('inicio'))
        
    datos_usuarios = []
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT id_usuario, correo, tipo_cuenta FROM usuarios")
        datos_usuarios = cursor.fetchall()
        bd.desconectar()
        
    return render_template('index.html', usuarios=datos_usuarios)

# ==========================================
# RUTA 2: ELIMINAR USUARIO (DINÁMICA)
# ==========================================
@app.route('/eliminar_usuario/<int:id_usuario>')
def eliminar_usuario(id_usuario):
    bd = ConexionBD()
    con = bd.conectar()
    
    if con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        con.commit()
        bd.desconectar()
        
    return redirect(url_for('inicio'))

# ==========================================
# RUTA 3: PROYECTOS MUSICALES
# ==========================================
@app.route('/proyectos', methods=['GET', 'POST'])
def proyectos():
    bd = ConexionBD()
    con = bd.conectar()
    
    if request.method == 'POST' and con:
        id_u = request.form.get('id_usuario')
        tit = request.form.get('titulo')
        gen = request.form.get('genero')
        if id_u and tit and gen:
            nuevo_proy = Proyecto(id_usuario=int(id_u), titulo_temp=tit, genero=gen)
            nuevo_proy.guardar_en_bd(con)
        bd.desconectar()
        return redirect(url_for('proyectos'))
        
    datos_proyectos = []
    if con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo 
            FROM proyectos p 
            INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
        """)
        datos_proyectos = cursor.fetchall()
        bd.desconectar()
        
    return render_template('proyectos.html', proyectos=datos_proyectos)

# ==========================================
# RUTA 4: ARCHIVOS DE AUDIO
# ==========================================
@app.route('/audios', methods=['GET', 'POST'])
def audios():
    bd = ConexionBD()
    con = bd.conectar()
    
    if request.method == 'POST' and con:
        id_p = request.form.get('id_proyecto')
        cat = request.form.get('categoria')
        formato = request.form.get('formato')
        tam = request.form.get('tamano')
        ruta = request.form.get('ruta')
        
        if id_p and cat and formato and tam and ruta:
            nuevo_audio = ArchivoAudio(
                id_proyecto=int(id_p), 
                categoria=cat, 
                formato=formato, 
                tamano_mb=float(tam), 
                url_almacen=ruta
            )
            nuevo_audio.guardar_en_bd(con)
        bd.desconectar()
        return redirect(url_for('audios'))
        
    datos_audios = []
    if con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT a.id_archivo, p.titulo_temp, a.categoria, a.formato, a.tamano_mb 
            FROM archivos_audio a 
            INNER JOIN proyectos p ON a.id_proyecto = p.id_proyecto
        """)
        datos_audios = cursor.fetchall()
        bd.desconectar()
        
    return render_template('audios.html', audios=datos_audios)

if __name__ == '__main__':
    print("Iniciando TrackManager Pro Web - Offten Studio...")
    app.run(debug=True, port=5000)