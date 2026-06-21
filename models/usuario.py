class Usuario:
    def __init__(self, correo: str, tipo_cuenta: str):
        self.correo = correo
        self.tipo_cuenta = tipo_cuenta  
        self.sesion_iniciada = False

    def guardar_en_bd(self, conexion):
        try:
            cursor = conexion.cursor() 
            sql = "INSERT INTO usuarios (correo, tipo_cuenta) VALUES (%s, %s)"
            valores = (self.correo, self.tipo_cuenta)
            
            cursor.execute(sql, valores)
            conexion.commit() 
            
            print(f"💾 ¡Éxito! Usuario '{self.correo}' guardado permanentemente en MySQL.")
        except Exception as e:
            print(f"❌ Error al intentar guardar en la base de datos: {e}")

    @staticmethod
    def mostrar_todos(conexion):
        """Busca todos los usuarios en la base de datos y los imprime en consola"""
        try:
            cursor = conexion.cursor()
            # El comando SELECT trae la información de las columnas que le pidamos
            cursor.execute("SELECT id_usuario, correo, tipo_cuenta, fecha_registro FROM usuarios")
            registros = cursor.fetchall() # fetchall() significa "trae todas las filas encontradas"
            
            print("\n" + "-"*40)
            print("📋 USUARIOS EN EL SISTEMA:")
            print("-"*40)
            
            if not registros:
                print("No hay ningún usuario registrado todavía.")
            else:
                for fila in registros:
                    print(f"ID: {fila[0]} | Correo: {fila[1]} | Tipo: {fila[2]}")
            print("-"*40)
            
        except Exception as e:
            print(f"❌ Error al intentar leer la base de datos: {e}")

    def iniciar_sesion(self) -> bool:
        self.sesion_iniciada = True
        print(f"✅ Sesión iniciada para: {self.correo} ({self.tipo_cuenta})")
        return True