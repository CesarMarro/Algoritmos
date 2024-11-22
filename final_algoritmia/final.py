# final.py

import tkinter as tk
import math
import argparse
import sys
from logica import (
    cargar_oraciones, 
    IndiceInvertido, 
    buscar_substring, 
    buscar_substring_indice_invertido
)

# GUI con navegación por páginas y profiling
class MotorBusquedaGUI:
    def __init__(self, root, oraciones, indice_invertido):
        self.root = root
        self.oraciones = oraciones
        self.indice_invertido = indice_invertido
        self.resultados = []
        self.pagina_actual = 0
        self.resultados_por_pagina = 20

        # Configuración de la ventana principal
        self.root.title("Motor de Búsqueda - Harry Potter")
        self.root.geometry("800x600")

        # Frame superior para controles de búsqueda y navegación
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10, padx=20, fill=tk.X)

        # Etiqueta de búsqueda
        self.label_busqueda = tk.Label(self.control_frame, text="Ingresa tu búsqueda:", font=("Arial", 14))
        self.label_busqueda.pack(side=tk.LEFT, padx=(0, 10))

        # Entrada de búsqueda
        self.entry_busqueda = tk.Entry(self.control_frame, font=("Arial", 14), width=30)
        self.entry_busqueda.pack(side=tk.LEFT, padx=(0, 10))

        # Botón de búsqueda
        self.boton_buscar = tk.Button(self.control_frame, text="Buscar", command=self.realizar_busqueda, font=("Arial", 14))
        self.boton_buscar.pack(side=tk.LEFT, padx=(0, 20))

        # Botón Anterior
        self.boton_anterior = tk.Button(self.control_frame, text="Anterior", command=self.pagina_anterior, state=tk.DISABLED, font=("Arial", 12))
        self.boton_anterior.pack(side=tk.LEFT, padx=(0, 10))

        # Botón Siguiente
        self.boton_siguiente = tk.Button(self.control_frame, text="Siguiente", command=self.pagina_siguiente, state=tk.DISABLED, font=("Arial", 12))
        self.boton_siguiente.pack(side=tk.LEFT)

        # Etiqueta para mostrar la cantidad de resultados
        self.label_cantidad = tk.Label(root, text="", font=("Arial", 12))
        self.label_cantidad.pack(pady=5)

        # Contenedor de resultados
        self.resultados_frame = tk.Frame(root)
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Indicador de página actual
        self.label_pagina = tk.Label(root, text="", font=("Arial", 12))
        self.label_pagina.pack(pady=5)

    def realizar_busqueda(self):
        query = self.entry_busqueda.get().strip()
        if not query:
            self.mostrar_mensaje("Por favor, ingresa un término de búsqueda.")
            return

        # Realizar búsquedas con profiling
        resultados_lineal = buscar_substring(self.oraciones, query)
        resultados_indice = buscar_substring_indice_invertido(self.indice_invertido, self.oraciones, query)

        # Puedes comparar los resultados si lo deseas
        # Por ahora, usaremos los resultados de la búsqueda lineal para la GUI
        self.resultados = resultados_lineal
        self.pagina_actual = 0

        if not self.resultados:
            self.mostrar_mensaje("No se encontraron resultados.")
            self.label_cantidad.config(text="")
            self.label_pagina.config(text="")
            self.boton_anterior.config(state=tk.DISABLED)
            self.boton_siguiente.config(state=tk.DISABLED)
            print("----------------------------")  # Divisor después de la búsqueda
            return

        # Actualizar la etiqueta de cantidad de resultados
        total_resultados = len(self.resultados)
        self.label_cantidad.config(text=f"Se encontraron {total_resultados} resultado(s).")

        # Mostrar resultados de la primera página
        self.mostrar_resultados()

        print("----------------------------")  # Divisor después de la búsqueda

    def mostrar_mensaje(self, mensaje):
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        etiqueta = tk.Label(self.resultados_frame, text=mensaje, font=("Arial", 14), fg="red")
        etiqueta.pack()

    def mostrar_resultados(self):
        # Limpiar el marco de resultados
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        # Determinar rango de resultados para la página actual
        inicio = self.pagina_actual * self.resultados_por_pagina
        fin = min(inicio + self.resultados_por_pagina, len(self.resultados))
        pagina_resultados = self.resultados[inicio:fin]

        # Mostrar resultados en la página actual
        for idx, oracion in pagina_resultados:
            etiqueta = tk.Label(
                self.resultados_frame, 
                text=f"[{idx}] {oracion}", 
                font=("Arial", 12), 
                wraplength=750, 
                anchor="w", 
                justify="left"
            )
            etiqueta.pack(anchor="w", pady=5)

        # Actualizar indicador de página
        total_paginas = math.ceil(len(self.resultados) / self.resultados_por_pagina)
        self.label_pagina.config(text=f"Página {self.pagina_actual + 1} de {total_paginas}")

        # Actualizar estado de botones de navegación
        self.actualizar_botones()

    def actualizar_botones(self):
        total_paginas = math.ceil(len(self.resultados) / self.resultados_por_pagina)
        if self.pagina_actual > 0:
            self.boton_anterior.config(state=tk.NORMAL)
        else:
            self.boton_anterior.config(state=tk.DISABLED)

        if self.pagina_actual < total_paginas - 1:
            self.boton_siguiente.config(state=tk.NORMAL)
        else:
            self.boton_siguiente.config(state=tk.DISABLED)

    def pagina_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_resultados()

    def pagina_siguiente(self):
        total_paginas = math.ceil(len(self.resultados) / self.resultados_por_pagina)
        if self.pagina_actual < total_paginas - 1:
            self.pagina_actual += 1
            self.mostrar_resultados()

# Configuración principal con profiling de carga de datos y memoria
def main():
    # Configuración de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Motor de Búsqueda en CSV con opción de multiprocessing.")
    parser.add_argument(
        '--multiprocessing', 
        action='store_true', 
        help='Activar multiprocessing para cargar datos más rápido.'
    )
    parser.add_argument(
        '--archivo',
        type=str,
        default='harry_potter_processed.csv',
        help='Ruta al archivo CSV de datos.'
    )
    args = parser.parse_args()

    archivo_csv = args.archivo  # Nombre del archivo CSV

    # Medir memoria antes de cargar datos
    memoria_pre_carga = obtener_uso_memoria()

    # Medir tiempo de carga y construir índice invertido
    oraciones, indice_invertido = cargar_oraciones(archivo_csv, use_multiprocessing=args.multiprocessing)

    # Calcular el incremento de memoria
    memoria_post_carga = obtener_uso_memoria()
    incremento_memoria = memoria_post_carga - memoria_pre_carga

    # Nota: Los mensajes de carga ya se manejan dentro de cargar_oraciones()

    # Crear la ventana principal y ejecutar la GUI
    root = tk.Tk()
    app = MotorBusquedaGUI(root, oraciones, indice_invertido)
    root.mainloop()

if __name__ == '__main__':
    # Importar funciones necesarias de logica.py
    from logica import obtener_uso_memoria
    main()
