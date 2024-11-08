import cv2
import sys

caminho = sys.argv[1]
imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)

if imagem is None:
    sys.exit(1)

print(f'Imagem carregada com dimensão {imagem.shape[0]} x {imagem.shape[1]}.')

nome_janela = caminho.split('/')[-1]
cv2.namedWindow(nome_janela, cv2.WINDOW_AUTOSIZE)
print('Imagem carregada com sucesso.')
print(f'formato da imagem: {imagem.shape[0]} x {imagem.shape[1]}')

limite_h = imagem.shape[0] // 2
limite_v = imagem.shape[1] // 2

q1 = imagem[:limite_h, :limite_v].copy()
q2 = imagem[:limite_h, limite_v:].copy()
q3 = imagem[limite_h:, :limite_v].copy()
q4 = imagem[limite_h:, limite_v:].copy()

imagem[:limite_h, :limite_v] = q4.copy()  # Q4 -> Q1
imagem[:limite_h, limite_v:] = q3.copy()  # Q3 -> Q2
imagem[limite_h:, :limite_v] = q2.copy()  # Q2 -> Q3
imagem[limite_h:, limite_v:] = q1.copy()  # Q1 -> Q4

cv2.imshow(nome_janela, imagem)
cv2.waitKey()
cv2.destroyAllWindows()

#cv2.imwrite('../figs/img02.png', imagem)