"""Main."""

# El ejecutor

import tkinter as tk
from logica import GestorAlumnos
from interfaz import AppEstudiantes


def main():
    """Inicializa la aplicación."""
    root = tk.Tk()
    gestor = GestorAlumnos()
    AppEstudiantes(root, gestor)
    root.mainloop()


if __name__ == "__main__":
    main()
