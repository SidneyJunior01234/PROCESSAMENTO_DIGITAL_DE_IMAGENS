import cv2
import numpy as np
import sys

ALTURA_MAX_SLIDER = 100
DECAI_MAX_SLIDER = 20
CENTRO_MAX_SLIDER = 100

imagem = cv2.imread(sys.argv[1])
imagem_borrada = cv2.GaussianBlur(imagem, (21, 21), 0)
resultado = imagem.copy()

def aplicar_tilt_shift(valor=0):
    altura = cv2.getTrackbarPos("Altura do Foco", "Tilt-Shift") / ALTURA_MAX_SLIDER
    decaimento = cv2.getTrackbarPos("Decaimento do Desfoque", "Tilt-Shift")
    centro = cv2.getTrackbarPos("Centro Vertical", "Tilt-Shift") / CENTRO_MAX_SLIDER
    
    altura_imagem, largura_imagem = imagem.shape[:2]
    centro_y = int(altura_imagem * centro)
    altura_foco = int(altura_imagem * altura)
    
    mascara = np.zeros((altura_imagem, largura_imagem), dtype=np.float32)
    mascara[max(0, centro_y - altura_foco // 2):min(altura_imagem, centro_y + altura_foco // 2), :] = 1
    
    if decaimento < 1:
        decaimento = 1
    elif decaimento % 2 == 0:
        decaimento += 1
    
    mascara = cv2.GaussianBlur(mascara, (decaimento, decaimento), sigmaX=decaimento, sigmaY=decaimento)
    
    global resultado
    resultado = (imagem * mascara[..., np.newaxis] + imagem_borrada * (1 - mascara[..., np.newaxis])).astype(np.uint8)
    cv2.imshow("Tilt-Shift", resultado)

cv2.namedWindow("Tilt-Shift")
cv2.createTrackbar("Altura do Foco", "Tilt-Shift", 50, ALTURA_MAX_SLIDER, aplicar_tilt_shift)
cv2.createTrackbar("Decaimento do Desfoque", "Tilt-Shift", 10, DECAI_MAX_SLIDER, aplicar_tilt_shift)
cv2.createTrackbar("Centro Vertical", "Tilt-Shift", 50, CENTRO_MAX_SLIDER, aplicar_tilt_shift)

cv2.imshow("Tilt-Shift", resultado)
aplicar_tilt_shift()

while True:
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('s'):
        cv2.imwrite("resultado_tiltshift.jpg", resultado)
        print("Imagem salva como resultado_tiltshift.jpg")
        break
    elif tecla != 255:
        break

cv2.destroyAllWindows()