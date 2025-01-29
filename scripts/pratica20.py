import cv2
import sys

image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)

if image is None:
    print(f"Erro ao carregar a imagem.")
    sys.exit()

# Elemento estruturante
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 10))

# Erosão
erosion = cv2.erode(image, kernel)

# Dilatação
dilation = cv2.dilate(image, kernel)

# Abertura
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# Fechamento
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# Abertura -> Fechamento
opening_closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

# Concatenação horizontal (apenas erosão neste exemplo)
result = cv2.hconcat([erosion])

cv2.imshow("morfologia", result)
cv2.waitKey(0)