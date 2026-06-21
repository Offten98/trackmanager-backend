import mysql.connector
from mysql.connector import Error

class ConexionBD:
    def __init__(self):
        # Credenciales por defecto de un servidor local (XAMPP/WAMP/MySQL Workbench)
        self.host = 'localhost'
        self.database = 'trackmanager_pro'
        self.user = 'root'
        self.password = ''  # Pon tu contraseña aquí si tu MySQL tiene una
        self.conexion = None

    def conectar(self):
        """Abre la conexión con la base de datos y la retorna."""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conexion.is_connected():
                print("✅ Conexión exitosa a la base de datos de TrackManager Pro")
                return self.conexion
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")
            return None

    def desconectar(self):
        """Cierra la conexión de forma segura."""
        if self.conexion is not None and self.conexion.is_connected():
            self.conexion.close()
            print("🔌 Conexión cerrada de forma segura.")