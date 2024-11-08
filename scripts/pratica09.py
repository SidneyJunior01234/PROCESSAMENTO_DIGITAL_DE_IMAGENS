import cv2
import numpy as np
import sys

KERNEL_LAPLACIANO = np.array([
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]
])

cap = cv2.VideoCapture(sys.argv[1])

if not cap.isOpened():
    print("Erro ao abrir o vídeo")
    sys.exit(1)

ret, frame = cap.read()
if not ret:
    print("Erro ao capturar o frame")
    sys.exit(1)

frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
max_laplaciano = np.zeros_like(frame_cinza, dtype=np.float32)
saida = np.zeros_like(frame)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('resultado_vaso.mp4', fourcc, fps, (width, height))

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break
    
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplaciano = cv2.filter2D(frame_cinza.astype(np.float32), -1, KERNEL_LAPLACIANO)
    mask = (laplaciano > max_laplaciano)
    max_laplaciano[mask] = laplaciano[mask]
    saida[mask] = frame[mask]

    out.write(saida)

cap.release()
out.release()
cv2.destroyAllWindows()