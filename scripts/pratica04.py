import cv2
import numpy as np
import sys

NBITS = 3

img_info_esc = cv2.imread(sys.argv[1])

if img_info_esc is None:
    sys.exit(1)

img_rec = np.zeros(img_info_esc.shape, dtype=np.uint8)

for linha in range(img_info_esc.shape[0]):
    for coluna in range(img_info_esc.shape[1]):
        for canal in range(3):
            pixel_esc = img_info_esc[linha, coluna, canal] & ((1 << NBITS) - 1)
            img_rec[linha, coluna, canal] = pixel_esc << (8 - NBITS)

cv2.imwrite('imagem_recuperada.png', img_rec)