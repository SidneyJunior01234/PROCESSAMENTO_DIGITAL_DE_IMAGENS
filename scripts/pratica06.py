import cv2
import numpy as np
import sys

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Nenhuma Câmera Encontrada.")
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_equalizado = cv2.equalizeHist(frame_cinza)
    imagem_final = np.concatenate(([frame_cinza, frame_equalizado]), axis=1)
    cv2.imshow("Imagem Equalizada", imagem_final)

    
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
