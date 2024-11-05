import os
import time
from PIL import Image
import csv
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import re

# Ruta a la carpeta con las imágenes
dataset_path = "dataset"
output_csv = "resultados_pokemon.csv"

def cargar_imagen(ruta_imagen):
    """Carga la imagen desde el disco."""
    return Image.open(ruta_imagen).convert("RGBA")

def color_dominante(imagen):
    """Determina el color dominante de una imagen en formato hexadecimal, ignorando solo los píxeles transparentes."""
    pixels = imagen.getdata()
    color_counts = {}

    for pixel in pixels:
        if pixel[3] > 0:  # Ignorar píxeles transparentes
            color_counts[pixel] = color_counts.get(pixel, 0) + 1

    # Encontrar el color más común
    dominant_color = max(color_counts, key=color_counts.get)
    
    # Convertir RGBA a hexadecimal
    dominant_color_hex = "#{:02x}{:02x}{:02x}".format(dominant_color[0], dominant_color[1], dominant_color[2])
    return dominant_color_hex

def contar_pixeles_transparentes(imagen):
    """Cuenta la cantidad de píxeles transparentes en la imagen."""
    pixels = imagen.getdata()
    transparent_pixels = sum(1 for pixel in pixels if pixel[3] == 0)
    return transparent_pixels

def orden_natural(texto):
    """Función para ordenar nombres de archivos de manera natural."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', texto)]

def procesar_imagen(args):
    """Procesa una imagen y retorna el resultado para escribir en el CSV."""
    ruta_imagen, nombre_imagen, numero_pokemon = args
    imagen = cargar_imagen(ruta_imagen)
    color_hex = color_dominante(imagen)
    transparent_pixels = contar_pixeles_transparentes(imagen)
    total_pixels = imagen.size[0] * imagen.size[1]
    color_pixels = total_pixels - transparent_pixels
    
    return {
        "numero_pokemon": numero_pokemon,
        "nombre_imagen": nombre_imagen,
        "color_dominante": color_hex,
        "pixeles_transparentes": transparent_pixels,
        "pixeles_color": color_pixels
    }

def get_sorted_file_list():
    """Obtiene y ordena la lista de archivos de imagen."""
    archivos = [f for f in os.listdir(dataset_path) if f.endswith(".png")]
    archivos = sorted(archivos, key=orden_natural)
    return archivos

def guardar_en_csv(resultados):
    """Guarda los resultados en un archivo CSV."""
    with open(output_csv, mode="w", newline="") as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=["numero_pokemon", "nombre_imagen", "color_dominante", "pixeles_transparentes", "pixeles_color"])
        escritor_csv.writeheader()
        escritor_csv.writerows(resultados)

def procesar_todas_imagenes():
    """Procesa todas las imágenes de manera secuencial y guarda los resultados en un archivo CSV."""
    resultados = []
    inicio_tiempo = time.time()
    numero_pokemon = 1

    archivos = get_sorted_file_list()
    for archivo in archivos:
        ruta_imagen = os.path.join(dataset_path, archivo)
        try:
            resultado = procesar_imagen((ruta_imagen, archivo, numero_pokemon))
            resultados.append(resultado)
            numero_pokemon += 1
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")

    fin_tiempo = time.time()
    tiempo_secuencial = fin_tiempo - inicio_tiempo
    print(f"Tiempo de ejecución (secuencial): {tiempo_secuencial:.2f} segundos")

    # Guardar resultados en un archivo CSV
    guardar_en_csv(resultados)

    return tiempo_secuencial

def procesar_todas_imagenes_parallel():
    """Procesa todas las imágenes usando multiprocesamiento y guarda los resultados en un archivo CSV."""
    inicio_tiempo = time.time()
    numero_pokemon = 1

    archivos = get_sorted_file_list()
    args_list = [(os.path.join(dataset_path, archivo), archivo, numero_pokemon + i) for i, archivo in enumerate(archivos)]
    num_nucleos = os.cpu_count()

    with ProcessPoolExecutor(max_workers=num_nucleos) as executor:
        resultados = list(executor.map(procesar_imagen, args_list))

    fin_tiempo = time.time()
    tiempo_paralelo = fin_tiempo - inicio_tiempo
    print(f"Tiempo de ejecución (paralelo con {num_nucleos} núcleos): {tiempo_paralelo:.2f} segundos")

    # Guardar resultados en un archivo CSV
    guardar_en_csv(resultados)

    return tiempo_paralelo

def procesar_todas_imagenes_parallel_hybrid():
    """Procesa todas las imágenes usando un enfoque híbrido de threading y multiprocesamiento."""
    inicio_tiempo = time.time()
    numero_pokemon = 1

    # Leer y ordenar los nombres de archivo usando threading
    with ThreadPoolExecutor() as thread_executor:
        future_archivos = thread_executor.submit(get_sorted_file_list)
        archivos = future_archivos.result()

    args_list = [(os.path.join(dataset_path, archivo), archivo, numero_pokemon + i) for i, archivo in enumerate(archivos)]
    num_nucleos = os.cpu_count()

    # Procesamiento intensivo en CPU usando multiprocesamiento
    with ProcessPoolExecutor(max_workers=num_nucleos) as process_executor:
        resultados = list(process_executor.map(procesar_imagen, args_list))

    fin_tiempo = time.time()
    tiempo_paralelo_hibrido = fin_tiempo - inicio_tiempo
    print(f"Tiempo de ejecución (paralelo híbrido con {num_nucleos} núcleos): {tiempo_paralelo_hibrido:.2f} segundos")

    # Escritura en CSV usando threading
    with ThreadPoolExecutor() as thread_executor:
        thread_executor.submit(guardar_en_csv, resultados)

    return tiempo_paralelo_hibrido

def mostrar_grafico_rendimiento(tiempos):
    """Genera una gráfica comparativa de los tiempos de ejecución."""
    import matplotlib.pyplot as plt

    modos = list(tiempos.keys())
    tiempo_valores = list(tiempos.values())

    plt.figure(figsize=(8, 5))
    plt.bar(modos, tiempo_valores, color=['blue', 'green', 'orange'])
    plt.xlabel('Modo de Ejecución')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Comparación de Tiempos de Ejecución')
    plt.show()

    for modo, tiempo in tiempos.items():
        if modo != 'Secuencial':
            mejora = ((tiempos['Secuencial'] - tiempo) / tiempos['Secuencial']) * 100
            print(f"Mejora de rendimiento con {modo}: {mejora:.2f}%")

if __name__ == "__main__":
    tiempos = {}

    print("Procesando imágenes de manera secuencial...")
    tiempo_secuencial = procesar_todas_imagenes()
    tiempos['Secuencial'] = tiempo_secuencial

    print(f"Procesando imágenes de manera paralela usando {os.cpu_count()} núcleos disponibles...")
    tiempo_paralelo = procesar_todas_imagenes_parallel()
    tiempos['Paralelo'] = tiempo_paralelo

    print("Procesando imágenes de manera híbrida (paralelo + threading)...")
    tiempo_paralelo_hibrido = procesar_todas_imagenes_parallel_hybrid()
    tiempos['Paralelo Híbrido'] = tiempo_paralelo_hibrido

    # Mostrar gráfica de comparación de rendimiento después del procesamiento
    mostrar_grafico_rendimiento(tiempos)
