import cv2
import numpy as np
import sys

TAMANHOS = [3, 11, 21]

def criar_mascara(tamanho):
    mascara = np.ones(shape=(tamanho,tamanho), dtype=np.float32) / (tamanho*tamanho)
    return mascara

def aplicar_mascara(ymg, mascara):
    imagem_filtrada = cv2.filter2D(frame_cinza, -1, mascara, borderType=cv2.BORDER_REPLICATE)
    return imagem_filtrada

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Nenhuma Câmera Encontrada.")
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_cinza = cv2.resize(frame_cinza, (352, 288))
    resultados = []
    for tamanho in TAMANHOS:
        mascara = criar_mascara(tamanho)
        resultado_filtro = aplicar_mascara(frame_cinza, mascara)
        resultados.append(resultado_filtro)

    imagem_final = np.concatenate((resultados), axis=1)
    cv2.imshow("Mascaras 3x3 11x11 21x21", imagem_final)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()