import cv2
import numpy as np
import sys

def swap_quadrants(image):
    h, w = image.shape[:2]
    cx, cy = w // 2, h // 2

    q0 = image[0:cy, 0:cx]
    q1 = image[0:cy, cx:w]
    q2 = image[cy:h, 0:cx]
    q3 = image[cy:h, cx:w]

    tmp = np.copy(q0)
    image[0:cy, 0:cx] = q3
    image[cy:h, cx:w] = tmp

    tmp = np.copy(q1)
    image[0:cy, cx:w] = q2
    image[cy:h, 0:cx] = tmp

def criar_filtro_homomorfico(shape, cutoff=30, low_gain=0.5, high_gain=2.0):
    rows, cols = shape
    center_x, center_y = cols // 2, rows // 2
    filter = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - center_y) ** 2 + (j - center_x) ** 2)
            filter[i, j] = (high_gain - low_gain) * (1 - np.exp(- (distance ** 2) / (2 * (cutoff ** 2)))) + low_gain

    planes = [filter, np.zeros_like(filter, dtype=np.float32)]
    return cv2.merge(planes)

def filtro_homomorfico(image, cutoff=30, low_gain=0.5, high_gain=2.0):
    dft_M = cv2.getOptimalDFTSize(image.shape[0])
    dft_N = cv2.getOptimalDFTSize(image.shape[1])
    padded = cv2.copyMakeBorder(image, 0, dft_M - image.shape[0], 0, dft_N - image.shape[1],
                                cv2.BORDER_CONSTANT, value=0)

    # Garante que as matrizes sejam float32
    planes = [np.float32(padded), np.zeros_like(padded, dtype=np.float32)]
    complex_image = cv2.merge(planes)

    cv2.dft(complex_image, complex_image)
    swap_quadrants(complex_image)

    filter = criar_filtro_homomorfico(padded.shape, cutoff, low_gain, high_gain)
    complex_image = cv2.mulSpectrums(complex_image, filter, 0)

    swap_quadrants(complex_image)
    cv2.idft(complex_image, complex_image)

    planes = cv2.split(complex_image)
    result = planes[0]
    result = result[:image.shape[0], :image.shape[1]]

    return cv2.normalize(result, None, 0, 1, cv2.NORM_MINMAX)

image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
if image is None:
    print(f"Erro ao abrir imagem {sys.argv[1]}")
    sys.exit()

result = filtro_homomorfico(image, cutoff=30, low_gain=0.5, high_gain=2.0)

cv2.imshow("Original", image)
cv2.imshow("Homomorphic Filter", result)
cv2.imwrite("../figs/imagem_filtrada.png", (result * 255).astype(np.uint8))
cv2.waitKey()