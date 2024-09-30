import numpy as np
import matplotlib.pyplot as plt

audio_path = "Shrek Retold Pelicula Completa (español latino).mp3"

with open(audio_path, "rb") as audio_file:
    audio_data = audio_file.read()

# Convertir los datos binarios a una lista de enteros
byte_values = list(audio_data)

# Omitir los primeros 10,000 bytes (ajusta este valor según sea necesario)
byte_values = byte_values[30000:]


threshold = 100  # Ajusta este umbral según la cantidad de silencio detectado

# Filtrar los valores que están por encima del umbral (ignorar momentos de silencio)
# filtered_values = [b for b in byte_values if b > threshold]

filtered_values = byte_values

# Mejorar la aleatoriedad combinando pares de bytes consecutivos
random_numbers = [
    (filtered_values[i] + filtered_values[i + 1]) % 10
    for i in range(0, len(filtered_values) - 1, 2)
]

# Limitar a 90,000 números aleatorios (300x300 matriz)
random_numbers = random_numbers[:90000]

# Convertir la lista en un array de 300x300
matrix = np.array(random_numbers).reshape(300, 300)

# Visualizar la matriz como imagen
plt.figure(figsize=(6, 6))
plt.imshow(matrix, cmap="gray", interpolation="none")
plt.title("Validación RNG a partir de numeros generados")
plt.colorbar()
plt.show()
