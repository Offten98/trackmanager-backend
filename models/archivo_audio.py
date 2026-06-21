class ArchivoAudio:
    def __init__(self, id_proyecto, categoria, formato, tamano_mb, url_almacen):
        self.id_proyecto = id_proyecto
        self.categoria = categoria
        self.formato = formato
        self.tamano_mb = tamano_mb
        self.url_almacen = url_almacen

    def guardar_en_bd(self, conexion):
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO archivos_audio (id_proyecto, categoria, formato, tamano_mb, url_almacen) VALUES (%s, %s, %s, %s, %s)"
            valores = (self.id_proyecto, self.categoria, self.formato, self.tamano_mb, self.url_almacen)
            
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"🔊 ¡Éxito! Archivo de '{self.categoria}' guardado en el Proyecto ID: {self.id_proyecto}")
        except Exception as e:
            print(f"❌ Error al guardar el archivo: {e}")

    def eliminar_de_bd(self, conexion, id_archivo):
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM archivos_audio WHERE id_archivo = %s"
            cursor.execute(sql, (id_archivo,))
            conexion.commit()
            print(f"Archivo con ID {id_archivo} eliminado correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar el archivo: {e}")
            return False