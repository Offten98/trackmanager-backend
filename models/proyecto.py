class Proyecto:
    def __init__(self, id_usuario: int, titulo_temp: str, genero: str):
        self.id_usuario = id_usuario 
        self.titulo_temp = titulo_temp
        self.genero = genero
        self.fase_actual = "Composición"
        self.notas_prod = ""

    def guardar_en_bd(self, conexion):
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO proyectos (id_usuario, titulo_temp, genero, fase_actual, notas_prod) VALUES (%s, %s, %s, %s, %s)"
            valores = (self.id_usuario, self.titulo_temp, self.genero, self.fase_actual, self.notas_prod)
            
            cursor.execute(sql, valores)
            conexion.commit() 
            
            print(f"🎵 ¡Éxito! Proyecto '{self.titulo_temp}' guardado y asignado al Usuario ID: {self.id_usuario}.")
        except Exception as e:
            print(f"❌ Error al guardar el proyecto en la base de datos: {e}")

    def actualizar_fase(self, conexion, id_proyecto, nueva_fase):
        try:
            cursor = conexion.cursor()
            # La instrucción SQL UPDATE modifica el campo específico usando el ID como filtro
            sql = "UPDATE proyectos SET fase_actual = %s WHERE id_proyecto = %s"
            cursor.execute(sql, (nueva_fase, id_proyecto))
            conexion.commit()
            print(f"Proyecto ID {id_proyecto} actualizado a la fase: {nueva_fase}")
            return True
        except Exception as e:
            print(f"Error al actualizar la fase del proyecto: {e}")
            return False

    def avanzar_fase(self, nueva_fase: str):
        self.fase_actual = nueva_fase
        print(f"📈 Proyecto '{self.titulo_temp}' avanzó a la fase: {self.fase_actual}")

    @staticmethod
    def mostrar_todos(conexion):
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT p.id_proyecto, p.titulo_temp, p.genero, p.fase_actual, u.correo 
            FROM proyectos p 
            INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
            """
            cursor.execute(sql)
            registros = cursor.fetchall()
            
            print("\n" + "-"*70)
            print("💿 PROYECTOS MUSICALES ACTIVOS:")
            print("-" * 70)
            
            if not registros:
                print("No hay ningún proyecto registrado todavía.")
            else:
                for fila in registros:
                    print(f"ID Proyecto: {fila[0]} | Canción: '{fila[1]}' ({fila[2]}) | Fase: {fila[3]} | Dueño: {fila[4]}")
            print("-" * 70)
            
        except Exception as e:
            print(f"❌ Error al intentar leer los proyectos: {e}")