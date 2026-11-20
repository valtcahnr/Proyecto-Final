"""Lógica."""

# El cuerpo

import json
import os


class GestorAlumnos:
    """Para definir la clase responsable de la lógica."""

    def __init__(self, nombre_archivo="alumnos.json"):
        """Inicializa la ruta del JSON y carga los alumnos guardados."""
        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )
        self.archivo_json = os.path.join(
            base_dir, nombre_archivo
        )
        self.alumnos = self.cargar_datos()

    def cargar_datos(self):
        """Para asegurar que los alumnos que se cargaron en ejecuciones anteriores reaparezcan al abrir la app."""
        if not os.path.exists(self.archivo_json):
            return []
        try:
            with open(
                self.archivo_json, "r", encoding="utf-8"
            ) as f:
                datos = json.load(f)
                return datos if isinstance(datos, list) else []
        except Exception:
            return []

    def guardar_datos(self):
        """Para guardar los datos y que no se pierdan al reiniciar el programa."""
        with open(
            self.archivo_json, "w", encoding="utf-8"
        ) as f:
            json.dump(
                self.alumnos, f, ensure_ascii=False, indent=4
            )

    @staticmethod
    def formatear_alumno(datos):
        """Para dar formato a los datos."""
        alumno = {
            clave: valor.strip() for clave, valor in datos.items()
        }
        alumno["nombre"] = alumno["nombre"].title()
        alumno["carrera"] = alumno["carrera"].title()
        return alumno

    def agregar_alumno(self, datos):
        """Formatea, registra y guarda un nuevo alumno en el JSON."""
        alumno = self.formatear_alumno(datos)
        self.alumnos.append(alumno)
        self.guardar_datos()
        return alumno

    def buscar_por_id(self, id_buscado):
        """Para buscar un alumno por su ID."""
        id_limpio = str(id_buscado).strip().lower()
        for indice, alumno in enumerate(self.alumnos):
            if str(alumno.get("id", "")).strip().lower() == id_limpio:
                return indice, alumno
        return -1, None

    def eliminar_por_indice(self, indice):
        """Elimina un alumno por su ID y actualiza el JSON."""
        if 0 <= indice < len(self.alumnos):
            eliminado = self.alumnos.pop(indice)
            self.guardar_datos()
            return eliminado
        return None

    def exportar_txt(self, ruta_archivo):
        """Exporta el listado de alumnos a un archivo de texto."""
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write("=== LISTA DE ESTUDIANTES REGISTRADOS ===\n\n")
            for idx, alumno in enumerate(self.alumnos, 1):
                f.write(f"Estudiante #{idx}\n")
                f.write(f"ID IEST: {alumno['id']}\n")
                f.write(f"Nombre: {alumno['nombre']}\n")
                f.write(f"Carrera: {alumno['carrera']}\n")
                f.write(f"Semestre: {alumno['semestre']}\n")
                f.write(f"Correo: {alumno['correo']}\n")
                f.write("-" * 30 + "\n")
