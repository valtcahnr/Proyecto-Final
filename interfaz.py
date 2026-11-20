"""Interfaz."""

# La vista

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class AppEstudiantes:
    """Configuración visual"""
    COLOR_FONDO = "#f4f6fb"
    COLOR_PRIMARIO = "#2f5bea"
    COLOR_PRIMARIO_HOVER = "#1e43c4"
    COLOR_PELIGRO = "#dc2626"
    COLOR_PELIGRO_HOVER = "#b91c1c"
    COLOR_TEXTO = "#7d8f3c"
    COLOR_TITULO = "#5f6f25"

    FUENTE = ("Segoe UI", 9)
    FUENTE_TITULO = ("Segoe UI", 14, "bold")

    def __init__(self, root, gestor):
        """Conecta la ventana a gestor"""
        self.root = root
        self.gestor = gestor

        self.configurar_estilos(self.root)
        self.root.title("Registro de estudiantes")
        self.centrar(self.root, 700, 250)
        self.construir_ventana_principal()

    def configurar_estilos(self, win):
        """Configura la apariencia"""
        win.configure(bg=self.COLOR_FONDO)
        estilo = ttk.Style(win)
        estilo.theme_use("clam")

        estilo.configure(".", background=self.COLOR_FONDO, 
                         foreground=self.COLOR_TEXTO, 
                         font=self.FUENTE)
        estilo.configure("Titulo.TLabel", 
                         font=self.FUENTE_TITULO, 
                         foreground=self.COLOR_TITULO)

        estilo.configure(
            "TButton",
            background=self.COLOR_PRIMARIO,
            foreground="white",
            padding=(12, 6),
            borderwidth=0,
            focuscolor=self.COLOR_PRIMARIO,
        )
        estilo.map("TButton", 
                   background=[("active", 
                                self.COLOR_PRIMARIO_HOVER)])

        estilo.configure("Peligro.TButton", background=self.COLOR_PELIGRO)
        estilo.map("Peligro.TButton", 
                   background=[("active", 
                                self.COLOR_PELIGRO_HOVER)])

        estilo.configure("TEntry", padding=6)
        estilo.configure("TCombobox", padding=6)

    @staticmethod
    def centrar(win, ancho, alto):
        """Centra las ventanas en el monitor"""
        x = (win.winfo_screenwidth() - ancho) // 2
        y = (win.winfo_screenheight() - alto) // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_ventana(self, padre, titulo, ancho, alto):
        win = tk.Toplevel(padre)
        win.title(titulo)
        win.configure(bg=self.COLOR_FONDO)
        self.centrar(win, ancho, alto)
        return win

    @staticmethod
    def mostrar_datos(frame, alumno):
        ttk.Label(frame, text=f"ID: {alumno['id']}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"Nombre: {alumno['nombre']}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"Carrera: {alumno['carrera']}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"Semestre: {alumno['semestre']}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"Correo: {alumno['correo']}").pack(anchor="w", pady=2)

    def construir_ventana_principal(self):
        ttk.Label(self.root, text="Registro de estudiantes", style="Titulo.TLabel").pack(padx=30, pady=30)
        ttk.Label(self.root, text="¿Qué desea hacer?").pack(padx=20, pady=10)

        botones = ttk.Frame(self.root)
        botones.pack(pady=10)

        ttk.Button(botones, text="Guardar", width=12, command=self.abrir_guardar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Buscar", width=12, command=self.abrir_buscar).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="Eliminar", width=12, command=self.abrir_eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(botones, text="Imprimir", width=12, command=self.abrir_imprimir).grid(row=0, column=3, padx=5)
        ttk.Button(botones, text="Salir", width=12, command=self.salir).grid(row=0, column=4, padx=5)

    def salir(self):
        if messagebox.askyesno("Salir", "¿Desea salir de la aplicación?"):
            self.root.destroy()

    def abrir_guardar(self):
        ventana_guardar = self.crear_ventana(self.root, "Registro de estudiantes", 700, 480)

        campos = [
            ("id", "ID IEST"),
            ("nombre", "Nombre del alumno"),
            ("carrera", "Carrera"),
            ("semestre", "Semestre"),
            ("correo", "Correo"),
        ]
        entradas = {}

        def leer_campos():
            datos = {clave: entradas[clave].get().strip() for clave, _ in campos}
            if "" in datos.values():
                messagebox.showwarning("Datos incompletos", "Llena todos los campos.", parent=ventana_guardar)
                return None
            return datos

        def limpiar():
            for clave, _ in campos:
                entradas[clave].delete(0, tk.END)
            entradas["id"].focus()

        def agregar():
            datos = leer_campos()
            if datos is None:
                return
            if messagebox.askyesno("Confirmar", "¿Desea agregar a este alumno?", parent=ventana_guardar):
                self.gestor.agregar_alumno(datos)
                messagebox.showinfo("Operación exitosa", "¡Alumno agregado correctamente!", parent=ventana_guardar)
            limpiar()

        def salir_guardar():
            if not messagebox.askyesno("Salir", "¿Está seguro de que quiere salir?", parent=ventana_guardar):
                return

            hay_texto = any(entradas[clave].get().strip() != "" for clave, _ in campos)
            if not hay_texto:
                ventana_guardar.destroy()
                return

            salir_confirmado = messagebox.askyesno(
                "Datos sin guardar",
                "Tienes datos escritos que no se han guardado.\n¿Está seguro de que desea salir y perder los cambios?",
                parent=ventana_guardar,
            )
            if salir_confirmado:
                ventana_guardar.destroy()

        ttk.Label(ventana_guardar, text="Registro de estudiantes", style="Titulo.TLabel").pack(padx=20, pady=20)

        formulario = ttk.Frame(ventana_guardar)
        formulario.pack(padx=30, pady=10)

        for fila, (clave, texto) in enumerate(campos):
            ttk.Label(formulario, text=f"{texto}:").grid(row=fila, column=0, sticky="e", padx=5, pady=8)
            if clave == "semestre":
                entradas[clave] = ttk.Combobox(formulario, values=list(range(1, 13)), width=57)
            else:
                entradas[clave] = ttk.Entry(formulario, width=60)
            entradas[clave].grid(row=fila, column=1, padx=5, pady=8)

        botones_guardar = ttk.Frame(ventana_guardar)
        botones_guardar.pack(pady=20)

        ttk.Button(botones_guardar, text="Agregar", width=12, command=agregar).grid(row=0, column=0, padx=5)
        ttk.Button(botones_guardar, text="Limpiar", width=12, command=limpiar).grid(row=0, column=1, padx=5)
        ttk.Button(botones_guardar, text="Salir", width=12, command=salir_guardar).grid(row=0, column=2, padx=5)

        ventana_guardar.bind("<Return>", lambda e: agregar())
        entradas["id"].focus()

    def abrir_buscar(self):
        ventana_buscar = self.crear_ventana(self.root, "Buscar estudiante", 520, 200)

        formulario = ttk.Frame(ventana_buscar)
        formulario.pack(padx=30, pady=30)

        ttk.Label(formulario, text="ID del estudiante:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entrada_id_buscar = ttk.Entry(formulario, width=30)
        entrada_id_buscar.grid(row=0, column=1, padx=5, pady=5)
        entrada_id_buscar.focus()

        def ejecutar_buscar():
            id_buscado = entrada_id_buscar.get().strip()
            if id_buscado == "":
                messagebox.showwarning("Campo vacío", "Ingresa un ID para buscar.", parent=ventana_buscar)
                return

            _, alumno_encontrado = self.gestor.buscar_por_id(id_buscado)

            if alumno_encontrado:
                messagebox.showinfo("¡Operación exitosa!", "Estudiante encontrado", parent=ventana_buscar)
                ventana_resultado = self.crear_ventana(ventana_buscar, "Resultado de la búsqueda", 380, 320)

                ttk.Label(ventana_resultado, text="¡Estudiante encontrado!", style="Titulo.TLabel").pack(pady=15)

                info_frame = ttk.Frame(ventana_resultado)
                info_frame.pack(padx=20, pady=5, anchor="w")
                self.mostrar_datos(info_frame, alumno_encontrado)

                ttk.Button(
                    ventana_resultado, text="Cerrar", width=10, command=ventana_resultado.destroy
                ).pack(pady=15)
            else:
                messagebox.showerror(
                    "No encontrado", "No se encontró ningún estudiante con ese ID.", parent=ventana_buscar
                )

        def salir_buscar():
            if messagebox.askyesno("Salir", "¿Desea salir de la búsqueda?", parent=ventana_buscar):
                ventana_buscar.destroy()

        botones_buscar = ttk.Frame(ventana_buscar)
        botones_buscar.pack(pady=10)

        ttk.Button(botones_buscar, text="Buscar", width=12, command=ejecutar_buscar).grid(row=0, column=0, padx=5)
        ttk.Button(botones_buscar, text="Cerrar", width=12, command=salir_buscar).grid(row=0, column=1, padx=5)

        ventana_buscar.bind("<Return>", lambda e: ejecutar_buscar())

    def abrir_eliminar(self):
        ventana_eliminar = self.crear_ventana(self.root, "Eliminar estudiante", 560, 190)

        formulario = ttk.Frame(ventana_eliminar)
        formulario.pack(padx=30, pady=30)

        ttk.Label(formulario, text="ID del estudiante a eliminar:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entrada_id_buscar_e = ttk.Entry(formulario, width=30)
        entrada_id_buscar_e.grid(row=0, column=1, padx=5, pady=5)
        entrada_id_buscar_e.focus()

        def ejecutar_buscar():
            id_buscado = entrada_id_buscar_e.get().strip()
            if id_buscado == "":
                messagebox.showwarning("Campo vacío", "Ingresa un ID para buscar.", parent=ventana_eliminar)
                return

            indice_e, alumno_encontrado_e = self.gestor.buscar_por_id(id_buscado)

            if alumno_encontrado_e:
                messagebox.showinfo("Estudiante", "Estudiante encontrado", parent=ventana_eliminar)
                ventana_resultado_e = self.crear_ventana(ventana_eliminar, "Eliminar", 380, 330)

                ttk.Label(ventana_resultado_e, text="Estudiante a eliminar", style="Titulo.TLabel").pack(pady=15)

                info_frame = ttk.Frame(ventana_resultado_e)
                info_frame.pack(padx=20, pady=5, anchor="w")
                self.mostrar_datos(info_frame, alumno_encontrado_e)

                def eliminar_alumno():
                    if messagebox.askyesno(
                        "Confirmar",
                        "¿Está completamente seguro de eliminar a este estudiante?\nLos datos se perderán de manera permanente.",
                        parent=ventana_resultado_e,
                    ):
                        self.gestor.eliminar_por_indice(indice_e)
                        messagebox.showinfo(
                            "Operación exitosa",
                            "Estudiante eliminado correctamente",
                            parent=ventana_resultado_e,
                        )
                        ventana_resultado_e.destroy()
                        ventana_eliminar.destroy()

                botones_resultado_e = ttk.Frame(ventana_resultado_e)
                botones_resultado_e.pack(pady=15)

                ttk.Button(
                    botones_resultado_e,
                    text="Eliminar",
                    width=12,
                    style="Peligro.TButton",
                    command=eliminar_alumno,
                ).grid(row=0, column=0, padx=5)
                ttk.Button(
                    botones_resultado_e, text="Cerrar", width=12, command=ventana_resultado_e.destroy
                ).grid(row=0, column=1, padx=5)
            else:
                messagebox.showerror(
                    "Error", "No se encontró ningún estudiante con ese ID.", parent=ventana_eliminar
                )

        def cancelar():
            if messagebox.askyesno("Salir", "¿Está seguro de que quiere salir?", parent=ventana_eliminar):
                ventana_eliminar.destroy()

        botones_eliminar = ttk.Frame(ventana_eliminar)
        botones_eliminar.pack(pady=10)

        ttk.Button(botones_eliminar, text="Buscar", width=12, command=ejecutar_buscar).grid(row=0, column=0, padx=5)
        ttk.Button(botones_eliminar, text="Cancelar", width=12, command=cancelar).grid(row=0, column=1, padx=5)

        ventana_eliminar.bind("<Return>", lambda e: ejecutar_buscar())

    def abrir_imprimir(self):
        if not self.gestor.alumnos:
            messagebox.showwarning("Error", "No hay estudiantes registrados para exportar.", parent=self.root)
            return

        ventana_imprimir = self.crear_ventana(self.root, "Imprimir", 460, 230)

        formulario = ttk.Frame(ventana_imprimir)
        formulario.pack(padx=30, pady=30)

        ttk.Label(
            formulario,
            text="¿Desea exportar la lista de estudiantes\na un archivo de texto?",
            justify="center",
        ).pack(padx=5, pady=5)

        def ejecutar_imprimir():
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                title="Guardar lista de estudiantes",
                parent=ventana_imprimir,
            )

            if archivo:
                try:
                    self.gestor.exportar_txt(archivo)
                    messagebox.showinfo(
                        "Operación exitosa",
                        f"Archivo guardado correctamente en:\n{archivo}",
                        parent=ventana_imprimir,
                    )
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}", parent=ventana_imprimir)

        def cancelar_imprimir():
            if messagebox.askyesno("Salir", "¿Está seguro de que quiere salir?", parent=ventana_imprimir):
                ventana_imprimir.destroy()

        botones_imprimir = ttk.Frame(ventana_imprimir)
        botones_imprimir.pack(pady=10)

        ttk.Button(botones_imprimir, text="Imprimir", width=12, command=ejecutar_imprimir).grid(row=0, column=0, padx=5)
        ttk.Button(botones_imprimir, text="Cancelar", width=12, command=cancelar_imprimir).grid(row=0, column=1, padx=5)
