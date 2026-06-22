from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.conexion import ConexionBD
from models.usuario import Usuario
from models.proyecto import Proyecto
from models.archivo_audio import ArchivoAudio
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "offten_studio_secure_key_2026"

# ==========================================
# RUTAS DE SEGURIDAD (LOGIN / REGISTRO / LOGOUT)
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_form = request.form.get('correo')
        pwd = request.form.get('password')
        
        bd = ConexionBD(); con = bd.conectar()
        if con:
            cursor = con.cursor()
            # Buscamos al usuario por su correo electrónico verdadero
            cursor.execute("SELECT id_usuario, correo, password FROM usuarios WHERE correo = %s", (correo_form,))
            usuario_bd = cursor.fetchone()
            bd.desconectar()
            
            # Validamos que exista y que la contraseña encriptada coincida
            if usuario_bd and check_password_hash(usuario_bd[2], pwd):
                session['logeado'] = True
                session['usuario_id'] = usuario_bd[0]
                session['usuario_correo'] = usuario_bd[1]
                return redirect(url_for('inicio'))
            else:
                flash("Credenciales incorrectas o el usuario no existe.", "error")
        else:
            flash("Error de conexión con la base de datos.", "error")
            
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro_público():
    if request.method == 'POST':
        correo_form = request.form.get('correo')
        tipo_form = request.form.get('tipo_cuenta')
        pwd = request.form.get('password')
        
        if correo_form and tipo_form and pwd:
            # Encriptamos la clave antes de guardarla en MySQL
            pwd_encriptada = generate_password_hash(pwd)
            
            bd = ConexionBD(); con = bd.conectar()
            if con:
                try:
                    cursor = con.cursor()
                    cursor.execute("""
                        INSERT INTO usuarios (correo, tipo_cuenta, password) 
                        VALUES (%s, %s, %s)
                    """, (correo_form, tipo_form, pwd_encriptada))
                    con.commit()
                    flash("Cuenta creada con éxito. Ya puedes iniciar sesión.", "exito")
                    bd.desconectar()
                    return redirect(url_for('login'))
                except Exception as e:
                    flash("Error: El correo electrónico ya está registrado.", "error")
                finally:
                    bd.desconectar()
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==========================================
# GESTIÓN DE USUARIOS
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def inicio():
    if 'logeado' not in session: return redirect(url_for('login'))
    
    bd = ConexionBD(); con = bd.conectar()
    if request.method == 'POST' and con:
        correo_form = request.form.get('correo')
        tipo_form = request.form.get('tipo_cuenta')
        pwd_form = request.form.get('password')
        if correo_form and tipo_form and pwd_form:
            pwd_encriptada = generate_password_hash(pwd_form)
            try:
                cursor = con.cursor()
                cursor.execute("INSERT INTO usuarios (correo, tipo_cuenta, password) VALUES (%s, %s, %s)", (correo_form, tipo_form, pwd_encriptada))
                con.commit()
            except Exception as e:
                flash("Error al guardar el usuario.", "error")
        bd.desconectar()
        return redirect(url_for('inicio'))
        
    datos_usuarios = []
    if con:
        cursor = con.cursor()
        busqueda = request.args.get('q', '').strip()
        if busqueda:
            cursor.execute("SELECT id_usuario, correo, tipo_cuenta FROM usuarios WHERE correo LIKE %s", (f"%{busqueda}%",))
        else:
            cursor.execute("SELECT id_usuario, correo, tipo_cuenta FROM usuarios")
        datos_usuarios = cursor.fetchall(); bd.desconectar()
    return render_template('index.html', usuarios=datos_usuarios)

@app.route('/eliminar_usuario/<int:id_usuario>')
def eliminar_usuario(id_usuario):
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM proyectos WHERE id_usuario = %s", (id_usuario,))
        tiene_proyectos = cursor.fetchone()[0]
        if tiene_proyectos > 0:
            flash("ERROR: No puedes eliminar este usuario porque tiene proyectos musicales activos.", "error")
        else:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            con.commit()
        bd.desconectar()
    return redirect(url_for('inicio'))

@app.route('/editar_usuario/<int:id_usuario>', methods=['GET', 'POST'])
def editar_usuario(id_usuario):
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
    if request.method == 'POST' and con:
        nuevo_correo = request.form.get('correo')
        nuevo_tipo = request.form.get('tipo_cuenta')
        cursor = con.cursor()
        cursor.execute("UPDATE usuarios SET correo = %s, tipo_cuenta = %s WHERE id_usuario = %s", (nuevo_correo, nuevo_tipo, id_usuario))
        con.commit(); bd.desconectar()
        return redirect(url_for('inicio'))
    usuario_actual = None
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT id_usuario, correo, tipo_cuenta FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario_actual = cursor.fetchone(); bd.desconectar()
    return render_template('editar_usuario.html', u=usuario_actual)

# ==========================================
# GESTIÓN DE PROYECTOS MUSICALES
# ==========================================
@app.route('/proyectos', methods=['GET', 'POST'])
def proyectos():
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
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
        busqueda = request.args.get('q', '').strip()
        if busqueda:
            cursor.execute("SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo FROM proyectos p INNER JOIN usuarios u ON p.id_usuario = u.id_usuario WHERE p.titulo_temp LIKE %s OR p.genero LIKE %s", (f"%{busqueda}%", f"%{busqueda}%"))
        else:
            cursor.execute("SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo FROM proyectos p INNER JOIN usuarios u ON p.id_usuario = u.id_usuario")
        datos_proyectos = cursor.fetchall(); bd.desconectar()
    return render_template('proyectos.html', proyectos=datos_proyectos)

@app.route('/eliminar_proyecto/<int:id_proyecto>')
def eliminar_proyecto(id_proyecto):
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM archivos_audio WHERE id_proyecto = %s", (id_proyecto,))
        tiene_audios = cursor.fetchone()[0]
        if tiene_audios > 0:
            flash("ERROR: No puedes eliminar este proyecto porque tiene stems o audios vinculados.", "error")
        else:
            cursor.execute("DELETE FROM proyectos WHERE id_proyecto = %s", (id_proyecto,))
            con.commit()
        bd.desconectar()
    return redirect(url_for('proyectos'))

@app.route('/editar_proyecto/<int:id_proyecto>', methods=['GET', 'POST'])
def editar_proyecto(id_proyecto):
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
    if request.method == 'POST' and con:
        tit = request.form.get('titulo')
        gen = request.form.get('genero')
        fas = request.form.get('fase')
        cursor = con.cursor()
        cursor.execute("UPDATE proyectos SET titulo_temp=%s, genero=%s, fase_actual=%s WHERE id_proyecto=%s", (tit, gen, fas, id_proyecto))
        con.commit(); bd.desconectar()
        return redirect(url_for('proyectos'))
    p_actual = None
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT id_proyecto, titulo_temp, genero, fase_actual FROM proyectos WHERE id_proyecto = %s", (id_proyecto,))
        p_actual = cursor.fetchone(); bd.desconectar()
    return render_template('editar_proyecto.html', p=p_actual)

# ==========================================
# GESTIÓN DE ARCHIVOS DE AUDIO
# ==========================================
@app.route('/audios', methods=['GET', 'POST'])
def audios():
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
    if request.method == 'POST' and con:
        id_p = request.form.get('id_proyecto')
        cat = request.form.get('categoria')
        formato = request.form.get('formato')
        tam = request.form.get('tamano')
        ruta = request.form.get('ruta')
        if id_p and cat and formato and tam and ruta:
            nuevo_audio = ArchivoAudio(id_proyecto=int(id_p), categoria=cat, formato=formato, tamano_mb=float(tam), url_almacen=ruta)
            nuevo_audio.guardar_en_bd(con)
        bd.desconectar()
        return redirect(url_for('audios'))
    datos_audios = []
    if con:
        cursor = con.cursor()
        busqueda = request.args.get('q', '').strip()
        if busqueda:
            cursor.execute("SELECT a.id_archivo, p.titulo_temp, a.categoria, a.formato, a.tamano_mb FROM archivos_audio a INNER JOIN proyectos p ON a.id_proyecto = p.id_proyecto WHERE p.titulo_temp LIKE %s OR a.categoria LIKE %s", (f"%{busqueda}%", f"%{busqueda}%"))
        else:
            cursor.execute("SELECT a.id_archivo, p.titulo_temp, a.categoria, a.formato, a.tamano_mb FROM archivos_audio a INNER JOIN proyectos p ON a.id_proyecto = p.id_proyecto")
        datos_audios = cursor.fetchall(); bd.desconectar()
    return render_template('audios.html', audios=datos_audios)

@app.route('/eliminar_audio/<int:id_archivo>')
def eliminar_audio(id_archivo):
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
    if con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM archivos_audio WHERE id_archivo = %s", (id_archivo,))
        con.commit(); bd.desconectar()
    return redirect(url_for('audios'))

@app.route('/editar_audio/<int:id_archivo>', methods=['GET', 'POST'])
def editar_audio(id_archivo):
    if 'logeado' not in session: return redirect(url_for('login'))
    bd = ConexionBD(); con = bd.conectar()
    if request.method == 'POST' and con:
        cat = request.form.get('categoria')
        formato = request.form.get('formato')
        tam = request.form.get('tamano')
        ruta = request.form.get('ruta')
        cursor = con.cursor()
        cursor.execute("UPDATE archivos_audio SET categoria=%s, formato=%s, tamano_mb=%s, url_almacen=%s WHERE id_archivo=%s", (cat, formato, tam, ruta, id_archivo))
        con.commit(); bd.desconectar()
        return redirect(url_for('audios'))
    a_actual = None
    if con:
        cursor = con.cursor()
        cursor.execute("SELECT id_archivo, categoria, formato, tamano_mb, url_almacen FROM archivos_audio WHERE id_archivo = %s", (id_archivo,))
        a_actual = cursor.fetchone(); bd.desconectar()
    return render_template('editar_audio.html', a=a_actual)

if __name__ == '__main__':
    app.run(debug=True, port=5000)