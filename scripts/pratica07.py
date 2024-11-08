import cv2
import sys
import numpy as np

THRESHOLD = 0.8
NBINS = 64  
RANGES = [0, 256]
HIST_ANTERIOR = None

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Nenhuma Câmera Encontrada.")
    sys.exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cv2.namedWindow('Motion Detector', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Motion Detector', 640, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray_frame], [0], None, [NBINS], RANGES)
    cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)

    if HIST_ANTERIOR is not None:
        difference = cv2.compareHist(HIST_ANTERIOR, hist, cv2.HISTCMP_CORREL)
        if difference < THRESHOLD:
            print("Alarme: Movimento detectado!")

    HIST_ANTERIOR = hist.copy()
    cv2.imshow("Motion Detector", frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()