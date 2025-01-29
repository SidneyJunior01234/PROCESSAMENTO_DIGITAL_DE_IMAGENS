import cv2
import sys

# Carregar a imagem em escala de cinza
imagem = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

if imagem is None:
    print(f"Não foi possível abrir {sys.argv[1]}")
    sys.exit(0)

# Aplicar limiarização binária usando OTSU
_, imagem = cv2.threshold(imagem, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Encontrar contornos
contornos, _ = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Converter a imagem de escala de cinza para BGR
imagem = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)

# Criar arquivo SVG para salvar os contornos
try:
    with open("contornos.svg", "w") as file:
        file.write(f"<svg height=\"{imagem.shape[0]}\" width=\"{imagem.shape[1]}\" xmlns=\"http://www.w3.org/2000/svg\"> \n")
        
        for contorno in contornos:
            # Adicionar o início do caminho
            file.write(f"<path d=\"M {contorno[0][0][0]} {contorno[0][0][1]} ")
            
            # Adicionar os pontos do contorno
            for point in contorno[1:]:
                file.write(f"L{point[0][0]} {point[0][1]} ")
            
            # Fechar o caminho
            file.write("Z\" fill=\"#cccccc\" stroke=\"black\" stroke-width=\"1\" />\n")
            
            # Desenhar o contorno na imagem
            cv2.drawContours(imagem, [contorno], -1, (255, 0, 0))
        
        file.write("</svg>\n")
except IOError:
    print("Não foi possível abrir ou criar o arquivo contornos.svg")
    sys.exit(0)

total_pontos = sum(len(contour) for contour in contornos)
print(f"Total de pontos nos contornos: {total_pontos}")

# Mostrar a imagem com os contornos desenhados
cv2.imshow("imagem", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()