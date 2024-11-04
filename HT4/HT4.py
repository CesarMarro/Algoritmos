import os
import time
from PIL import Image
import csv

# Ruta a la carpeta con las imágenes
dataset_path = "dataset"
output_csv = "resultados_pokemon.csv"

def cargar_imagen(ruta_imagen):
    """Carga la imagen desde el disco."""
    return Image.open(ruta_imagen).convert("RGBA")

def color_dominante(imagen):
    """Determina el color dominante de una imagen en formato RGBA, ignorando solo los píxeles transparentes."""
    pixels = imagen.getdata()  # Obtenemos todos los píxeles de la imagen
    
    # Lista para almacenar colores y sus conteos [(color, conteo)]
    color_counts = []

    # Recorremos todos los píxeles y contamos los colores, ignorando los transparentes
    for pixel in pixels:
        if pixel[3] > 0:  # Ignoramos los píxeles transparentes
            found = False
            
            # Buscar si el color ya está en color_counts
            for i in range(len(color_counts)):
                if color_counts[i][0] == pixel:
                    # Si encontramos el color, incrementamos el conteo
                    color_counts[i] = (color_counts[i][0], color_counts[i][1] + 1)
                    found = True
                    break
            
            # Si el color no está en la lista, lo añadimos con un conteo inicial de 1
            if not found:
                color_counts.append((pixel, 1))
    
    # Encontrar el color más común en la lista
    most_common_color = None
    max_count = 0
    for color, count in color_counts:
        if count > max_count:
            most_common_color = color
            max_count = count

    # Retornar el color dominante en formato RGBA
    return most_common_color if most_common_color else (0, 0, 0, 0)  # (0, 0, 0, 0) si todos los píxeles son transparentes

def contar_pixeles_transparentes(imagen):
    """Cuenta la cantidad de píxeles transparentes en la imagen."""
    pixels = imagen.getdata()
    transparent_pixels = 0

    # Contamos manualmente los píxeles transparentes
    for pixel in pixels:
        if pixel[3] == 0:
            transparent_pixels += 1

    return transparent_pixels

def procesar_imagen(ruta_imagen, numero_pokemon):
    """Procesa una imagen y retorna el resultado para escribir en el CSV."""
    imagen = cargar_imagen(ruta_imagen)
    color_rgba = color_dominante(imagen)  # Cambiado para obtener RGBA en lugar de RGB o hexadecimal
    transparent_pixels = contar_pixeles_transparentes(imagen)
    total_pixels = imagen.size[0] * imagen.size[1]
    color_pixels = total_pixels - transparent_pixels
    
    return {
        "numero_pokemon": numero_pokemon,
        "color_dominante": color_rgba,  # Almacenamos el color como una tupla RGBA
        "pixeles_transparentes": transparent_pixels,
        "pixeles_color": color_pixels
    }

def procesar_todas_imagenes():
    """Procesa todas las imágenes en el dataset y guarda los resultados en un archivo CSV."""
    resultados = []
    numero_pokemon = 1
    
    # Medir tiempo de ejecución
    inicio_tiempo = time.time()
    
    # Listamos y ordenamos los archivos para asegurar el procesamiento en orden numérico o alfabético
    archivos = sorted(os.listdir(dataset_path))  # Ordenar los archivos

    for archivo in archivos:
        if archivo.endswith(".png"):
            ruta_imagen = os.path.join(dataset_path, archivo)
            try:
                resultado = procesar_imagen(ruta_imagen, numero_pokemon)
                resultados.append(resultado)
                numero_pokemon += 1
            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")
    
    fin_tiempo = time.time()
    print(f"Tiempo de ejecución: {fin_tiempo - inicio_tiempo:.2f} segundos")
    
    # Guardar resultados en un archivo CSV
    with open(output_csv, mode="w", newline="") as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=["numero_pokemon", "color_dominante", "pixeles_transparentes", "pixeles_color"])
        escritor_csv.writeheader()
        escritor_csv.writerows(resultados)

if __name__ == "__main__":
    procesar_todas_imagenes()
