import cv2
import numpy as np
import random
import sys

# Constantes para pontilhismo
PASSO = 5
DESVIO = 3
RAIO_INICIAL = 5

# Configuração inicial do Canny
CANNY_MINIMO = 50
CANNY_MAXIMO = 150

def gerar_mascara_pontilhismo(imagem):
    altura, largura = imagem.shape
    mascara = np.zeros((altura, largura), dtype=np.uint8)

    faixa_x = [(i * PASSO + PASSO // 2) for i in range(altura // PASSO)]
    faixa_y = [(i * PASSO + PASSO // 2) for i in range(largura // PASSO)]

    random.seed()
    random.shuffle(faixa_x)

    for x in faixa_x:
        random.shuffle(faixa_y)
        for y in faixa_y:
            desviado_x = x + random.randint(-DESVIO, DESVIO)
            desviado_y = y + random.randint(-DESVIO, DESVIO)

            desviado_x = max(0, min(altura - 1, desviado_x))
            desviado_y = max(0, min(largura - 1, desviado_y))

            cinza = imagem[desviado_x, desviado_y]
            cv2.circle(mascara, (desviado_y, desviado_x), RAIO_INICIAL, int(cinza), -1, lineType=cv2.LINE_AA)

    return mascara

def adicionar_bordas_canny_na_mascara(imagem, mascara):
    altura, largura = imagem.shape

    for fator_raio in range(1, 4):
        limite_inferior = fator_raio * CANNY_MINIMO
        limite_superior = fator_raio * CANNY_MAXIMO

        bordas = cv2.Canny(imagem, limite_inferior, limite_superior)

        for x in range(altura):
            for y in range(largura):
                if bordas[x, y] > 0:
                    cinza = int(imagem[x, y])
                    raio = max(1, RAIO_INICIAL - fator_raio)
                    cv2.circle(mascara, (y, x), raio, int(cinza), -1, lineType=cv2.LINE_AA)

    return mascara

def aplicar_mascara_na_imagem_colorida(imagem_colorida, mascara):
    # Converte a máscara para float32
    mascara_normalizada = mascara.astype(np.float32) / 255.0
    resultado = np.zeros_like(imagem_colorida, dtype=np.uint8)
    
    # Aplica a máscara em cada canal
    for c in range(3):  # Para os canais B, G, R
        resultado[:, :, c] = (imagem_colorida[:, :, c].astype(np.float32) * mascara_normalizada).astype(np.uint8)
    
    return resultado

imagem_colorida = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
if imagem_colorida is None:
    print("Erro ao carregar a imagem.")
    sys.exit()

# Converte a imagem para tons de cinza
imagem_cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)

# Gera a máscara de pontilhismo
mascara = gerar_mascara_pontilhismo(imagem_cinza)

# Adiciona as bordas detectadas pelo filtro Canny na máscara
mascara = adicionar_bordas_canny_na_mascara(imagem_cinza, mascara)

# Aplica a máscara à imagem colorida
resultado = aplicar_mascara_na_imagem_colorida(imagem_colorida, mascara)

# Exibe e salva o resultado
#cv2.imshow("Mascara", mascara)
cv2.imshow("Resultado Colorido", resultado)
#cv2.imwrite("resultado_colorido.jpg", resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()