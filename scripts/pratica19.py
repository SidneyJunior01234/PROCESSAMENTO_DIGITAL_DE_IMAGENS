import cv2
import sys

img = cv2.imread(sys.argv[1])

if img is None:
    print('Imagem não encontrada.')
    sys.exit()

img_color = img.copy()

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

with open('momentos.txt', 'w') as f:
    for i, cnt in enumerate(contours):
        # Verificar se o contorno é grande o suficiente
        if len(cnt) < 10:
            continue

        # Calcular os momentos
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        # Calcular os momentos de Hu
        huMoments = cv2.HuMoments(M).flatten()

        # Desenhar o contorno
        cv2.drawContours(img_color, [cnt], 0, (0, 0, 255), 2)

        # Colocar o número do contorno
        cv2.putText(img_color, str(i), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        # Salvar os momentos de Hu
        f.write(f"{i},")
        for h in huMoments:
            f.write(f"{h:.3f},")
        f.write('\n')

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', img_color)
cv2.imwrite('momento_count.png', img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()