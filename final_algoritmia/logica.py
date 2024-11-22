# logica.py

import csv
import psutil
import time
import sys
import multiprocessing
import math

# índice invertido desde cero
class IndiceInvertido:
    def __init__(self):
        self.datos = {} 

    def agregar(self, palabra, indice):
        if palabra not in self.datos:
            self.datos[palabra] = []
        self.datos[palabra].append(indice)

    def obtener(self, palabra):
        return self.datos.get(palabra, [])

# Función para obtener el uso actual de memoria en MB
def obtener_uso_memoria():
    proceso = psutil.Process()
    memoria = proceso.memory_info().rss / (1024 * 1024)  # Convertir bytes a MB
    return memoria

# Función auxiliar para imprimir resultados de profiling de manera concisa
def imprimir_resultado(descripcion, valor, limite, unidad, tipo='tiempo'):
    excede = valor > limite
    if excede:
        mensaje_excede = f"Advertencia: {descripcion} excede los {limite}{unidad}. Valor: {valor:.2f}{unidad}."
        print(mensaje_excede)
    else:
        mensaje_dentro = f"{descripcion} está dentro del límite de {limite}{unidad}. Valor: {valor:.2f}{unidad}."
        print(mensaje_dentro)

# Función de trabajo para procesar un chunk de filas
def procesar_chunk(args):
    rows, start_idx = args
    oraciones_parciales = []
    indice_invertido_parcial = IndiceInvertido()
    
    for i, row in enumerate(rows):
        if row:  # Asegurarse de que la fila no esté vacía
            oracion = row[0]
            oraciones_parciales.append(oracion)
            # Construir el índice invertido
            palabras = oracion.lower().split()
            for palabra in set(palabras):  # Usar set para evitar duplicados
                indice_invertido_parcial.agregar(palabra, start_idx + i)
    
    return oraciones_parciales, indice_invertido_parcial.datos

# Carga de datos del CSV con profiling, creación del índice invertido y opcionalmente multiprocessing
def cargar_oraciones(archivo_csv, use_multiprocessing=False):
    oraciones = []
    indice_invertido = IndiceInvertido()
    try:
        # Medir memoria antes de cargar datos
        memoria_pre_carga = obtener_uso_memoria()

        if use_multiprocessing:
            # Determinar el número de procesos a utilizar
            num_procesos = multiprocessing.cpu_count()
            print(f"Usando {num_procesos} procesos para cargar datos.")
        
            # Leer todo el archivo y dividirlo en chunks
            chunks = []
            chunk_size = 10000  # Número de filas por chunk
            with open(archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                current_chunk = []
                start_idx = 0
                for i, row in enumerate(reader):
                    current_chunk.append(row)
                    if (i + 1) % chunk_size == 0:
                        chunks.append((current_chunk, start_idx))
                        start_idx += len(current_chunk)
                        current_chunk = []
                # Añadir el último chunk si no está vacío
                if current_chunk:
                    chunks.append((current_chunk, start_idx))
            
            # Medir tiempo de carga
            inicio_carga = time.time()
        
            # Crear un pool de procesos y procesar los chunks en paralelo
            with multiprocessing.Pool(processes=num_procesos) as pool:
                resultados = pool.map(procesar_chunk, chunks)
        
            # Combinar los resultados parciales
            for oraciones_parciales, indice_invertido_parcial in resultados:
                oraciones.extend(oraciones_parciales)
                for palabra, indices in indice_invertido_parcial.items():
                    for indice in indices:
                        indice_invertido.agregar(palabra, indice)
        
            fin_carga = time.time()
            tiempo_carga = (fin_carga - inicio_carga) * 1000  # Convertir a milisegundos

        else:
            # Procesamiento secuencial sin multiprocessing
            print("Usando procesamiento secuencial para cargar datos.")
            inicio_carga = time.time()
            with open(archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if row:  # Asegurarse de que la fila no esté vacía
                        oracion = row[0]
                        oraciones.append(oracion)
                        # Construir el índice invertido
                        palabras = oracion.lower().split()
                        for palabra in set(palabras):  # Usar set para evitar duplicados
                            indice_invertido.agregar(palabra, i)
            fin_carga = time.time()
            tiempo_carga = (fin_carga - inicio_carga) * 1000  # Convertir a milisegundos

        # Medir memoria después de cargar datos
        memoria_post_carga = obtener_uso_memoria()
        incremento_memoria = memoria_post_carga - memoria_pre_carga

        # Verificar restricciones de carga
        imprimir_resultado(
            descripcion="Tiempo de carga de datos",
            valor=tiempo_carga,
            limite=500,
            unidad="ms",
            tipo='tiempo'
        )

        imprimir_resultado(
            descripcion="Incremento de memoria tras cargar datos",
            valor=incremento_memoria,
            limite=25,
            unidad="MB",
            tipo='memoria'
        )

        print("----------------------------")  # Divisor después de la carga de datos

    except FileNotFoundError:
        print(f"Error: El archivo {archivo_csv} no se encontró.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        sys.exit(1)
    return oraciones, indice_invertido

# Búsqueda de substrings con profiling (Búsqueda Lineal)
def buscar_substring(oraciones, query):
    resultados = []
    query_lower = query.lower()

    # Medir memoria antes de la búsqueda
    memoria_pre_busqueda = obtener_uso_memoria()

    # Medir tiempo de búsqueda
    inicio_busqueda = time.time()

    for i, oracion in enumerate(oraciones):
        if query_lower in oracion.lower():
            resultados.append((i, oracion))

    fin_busqueda = time.time()
    tiempo_busqueda = (fin_busqueda - inicio_busqueda) * 1000  # Convertir a milisegundos

    # Medir memoria después de la búsqueda
    memoria_post_busqueda = obtener_uso_memoria()
    incremento_memoria_busqueda = memoria_post_busqueda - memoria_pre_busqueda

    # Resumir resultados de la búsqueda lineal
    imprimir_resultado(
        descripcion="Tiempo de búsqueda lineal",
        valor=tiempo_busqueda,
        limite=500,
        unidad="ms",
        tipo='tiempo'
    )

    imprimir_resultado(
        descripcion="Incremento de memoria durante la búsqueda lineal",
        valor=incremento_memoria_busqueda,
        limite=25,
        unidad="MB",
        tipo='memoria'
    )

    return resultados

# Búsqueda utilizando Índice Invertido con profiling
def buscar_substring_indice_invertido(indice, oraciones, query):
    resultados = []
    query_lower = query.lower()

    # Medir memoria antes de la búsqueda
    memoria_pre_busqueda = obtener_uso_memoria()

    # Medir tiempo de búsqueda
    inicio_busqueda = time.time()

    # Asumimos que la búsqueda se realiza por palabras completas
    # Dividir la query en palabras
    palabras_query = query_lower.split()
    if not palabras_query:
        return resultados

    # Obtener conjuntos de índices para cada palabra en la query
    conjuntos_indices = []
    for palabra in palabras_query:
        conjuntos_indices.append(set(indice.obtener(palabra)))

    # Intersectar los conjuntos para obtener oraciones que contengan todas las palabras
    if conjuntos_indices:
        indices_comunes = set.intersection(*conjuntos_indices)
    else:
        indices_comunes = set()

    # Filtrar las oraciones que realmente contienen la subcadena (para manejar subcadenas parciales)
    for i in indices_comunes:
        if query_lower in oraciones[i].lower():
            resultados.append((i, oraciones[i]))

    fin_busqueda = time.time()
    tiempo_busqueda = (fin_busqueda - inicio_busqueda) * 1000  # Convertir a milisegundos

    # Medir memoria después de la búsqueda
    memoria_post_busqueda = obtener_uso_memoria()
    incremento_memoria_busqueda = memoria_post_busqueda - memoria_pre_busqueda

    # Resumir resultados de la búsqueda con índice invertido
    imprimir_resultado(
        descripcion="Tiempo de búsqueda con índice invertido",
        valor=tiempo_busqueda,  # <-- Aquí se corrigió el nombre de la variable
        limite=500,
        unidad="ms",
        tipo='tiempo'
    )

    imprimir_resultado(
        descripcion="Incremento de memoria durante la búsqueda con índice invertido",
        valor=incremento_memoria_busqueda,
        limite=25,
        unidad="MB",
        tipo='memoria'
    )

    return resultados
