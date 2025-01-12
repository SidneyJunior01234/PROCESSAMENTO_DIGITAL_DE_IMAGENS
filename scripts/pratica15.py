import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys

numero_de_clusters = 8
criterio_de_parada = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
n_rodadas = 10

imagem = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)

# Converter a imagem para um formato adequado para o K-Means
dados = imagem.reshape((-1,3))
dados = np.float32(dados)

resultados = []

for i in range(n_rodadas):
    ret, rotulos, centros = cv2.kmeans(dados, numero_de_clusters, None, criterio_de_parada, n_rodadas, cv2.KMEANS_RANDOM_CENTERS)

    # Converter os rótulos para a forma original da imagem
    centros = np.uint8(centros)
    resultado = centros[rotulos.flatten()]
    resultado_final = resultado.reshape((imagem.shape))
    resultados.append(resultado_final)

fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for i, ax in enumerate(axes.flat):
    ax.imshow(resultados[i])
    ax.set_title(f"Rodada {i+1}")
plt.tight_layout()
plt.show()
plt.savefig("resultado.png")