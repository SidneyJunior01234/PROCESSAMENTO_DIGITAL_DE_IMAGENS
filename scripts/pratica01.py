import cv2
import sys

caminho = sys.argv[1]
p1 = sys.argv[2:4]
p2 = sys.argv[4:]

img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)

imagem = img.copy()

if imagem is None:
    sys.exit(1)

print(f'Imagem carregada com dimensão {imagem.shape[0]} x {imagem.shape[1]}.')
nome_janela = caminho.split('/')[-1]

cv2.namedWindow(nome_janela, cv2.WINDOW_AUTOSIZE)

for linha in range(int(p1[0]), int(p2[0])):
    for coluna in range(int(p1[1]), int(p2[1])):
        imagem[linha, coluna] = 255 - imagem[linha, coluna]

cv2.imshow(nome_janela, imagem)
cv2.waitKey()
cv2.destroyAllWindows()
#cv2.imwrite('../figs/img01.png', imagem)