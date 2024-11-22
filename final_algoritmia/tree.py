import csv
import tkinter as tk
import psutil
import time
import sys
import math


# Clase para representar un nodo en el Trie
class TrieNode:
    def __init__(self):
        self.hijos = {}  # Diccionario de hijos (carácter -> nodo)
        self.fin_palabra = False  # Marca si este nodo representa el final de una palabra
        self.indices = []  # Lista de índices donde aparece esta palabra


# Clase para la estructura Trie
class Trie:
    def __init__(self):
        self.raiz = TrieNode()

    def agregar(self, palabra, indice):
        nodo_actual = self.raiz
        for char in palabra:
            if char not in nodo_actual.hijos:
                nodo_actual.hijos[char] = TrieNode()
            nodo_actual = nodo_actual.hijos[char]
        nodo_actual.fin_palabra = True
        nodo_actual.indices.append(indice)

    def buscar(self, prefijo):
        nodo_actual = self.raiz
        for char in prefijo:
            if char not in nodo_actual.hijos:
                return []  # Prefijo no encontrado
            nodo_actual = nodo_actual.hijos[char]
        return self._recuperar_palabras(nodo_actual, prefijo)

    def _recuperar_palabras(self, nodo, prefijo):
        resultados = []
        if nodo.fin_palabra:
            resultados.append((prefijo, nodo.indices))
        for char, hijo in nodo.hijos.items():
            resultados.extend(self._recuperar_palabras(hijo, prefijo + char))
        return resultados


# Función para obtener el uso actual de memoria en MB
def obtener_uso_memoria():
    proceso = psutil.Process()
    memoria = proceso.memory_info().rss / (1024 * 1024)  # Convertir bytes a MB
    return memoria


# Función auxiliar para imprimir resultados de profiling
def imprimir_resultado(descripcion, valor, limite, unidad, tipo='tiempo'):
    excede = valor > limite
    if excede:
        print(f"Advertencia: {descripcion} excede los {limite}{unidad}. Valor: {valor:.2f}{unidad}.")
    else:
        print(f"{descripcion} está dentro del límite de {limite}{unidad}. Valor: {valor:.2f}{unidad}.")


# Función para cargar datos y construir el Trie
def cargar_oraciones_con_trie(archivo_csv):
    oraciones = []
    trie = Trie()
    try:
        memoria_pre_carga = obtener_uso_memoria()
        inicio_carga = time.time()

        with open(archivo_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if row:
                    oracion = row[0]
                    oraciones.append(oracion)
                    palabras = oracion.lower().split()
                    for palabra in set(palabras):  # Usar set para evitar duplicados
                        trie.agregar(palabra, i)

        fin_carga = time.time()
        tiempo_carga = (fin_carga - inicio_carga) * 1000
        memoria_post_carga = obtener_uso_memoria()
        incremento_memoria = memoria_post_carga - memoria_pre_carga

        imprimir_resultado("Tiempo de carga de datos", tiempo_carga, 500, "ms")
        imprimir_resultado("Incremento de memoria tras cargar datos", incremento_memoria, 25, "MB")

    except FileNotFoundError:
        print(f"Error: El archivo {archivo_csv} no se encontró.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        sys.exit(1)

    return oraciones, trie


# Búsqueda con Trie y profiling
def buscar_en_trie(trie, oraciones, query):
    # Profiling inicial
    memoria_pre_busqueda = obtener_uso_memoria()
    inicio_busqueda = time.time()

    palabras_query = query.lower().split()
    if not palabras_query:
        return []

    resultados = []
    for palabra in palabras_query:
        resultados.extend(trie.buscar(palabra))

    indices_unicos = set()
    for _, indices in resultados:
        indices_unicos.update(indices)

    # Profiling final
    fin_busqueda = time.time()
    tiempo_busqueda = (fin_busqueda - inicio_busqueda) * 1000
    memoria_post_busqueda = obtener_uso_memoria()
    incremento_memoria = memoria_post_busqueda - memoria_pre_busqueda

    imprimir_resultado("Tiempo de búsqueda", tiempo_busqueda, 500, "ms")
    imprimir_resultado("Incremento de memoria durante la búsqueda", incremento_memoria, 25, "MB")

    return sorted(indices_unicos)


# GUI con navegación por páginas y Trie
class MotorBusquedaGUI:
    def __init__(self, root, oraciones, trie):
        self.root = root
        self.oraciones = oraciones
        self.trie = trie
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

        indices = buscar_en_trie(self.trie, self.oraciones, query)
        self.resultados = [(i, self.oraciones[i]) for i in indices]
        self.pagina_actual = 0

        if not self.resultados:
            self.mostrar_mensaje("No se encontraron resultados.")
            self.label_cantidad.config(text="")
            self.label_pagina.config(text="")
            self.boton_anterior.config(state=tk.DISABLED)
            self.boton_siguiente.config(state=tk.DISABLED)
            return

        total_resultados = len(self.resultados)
        self.label_cantidad.config(text=f"Se encontraron {total_resultados} resultado(s).")
        self.mostrar_resultados()

    def mostrar_mensaje(self, mensaje):
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        etiqueta = tk.Label(self.resultados_frame, text=mensaje, font=("Arial", 14), fg="red")
        etiqueta.pack()

    def mostrar_resultados(self):
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        inicio = self.pagina_actual * self.resultados_por_pagina
        fin = min(inicio + self.resultados_por_pagina, len(self.resultados))
        pagina_resultados = self.resultados[inicio:fin]

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

        total_paginas = math.ceil(len(self.resultados) / self.resultados_por_pagina)
        self.label_pagina.config(text=f"Página {self.pagina_actual + 1} de {total_paginas}")
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


# Cargar datos y lanzar la GUI
if __name__ == '__main__':
    archivo_csv = 'harry_potter_processed.csv'
    oraciones, trie = cargar_oraciones_con_trie(archivo_csv)

    root = tk.Tk()
    app = MotorBusquedaGUI(root, oraciones, trie)
    root.mainloop()
