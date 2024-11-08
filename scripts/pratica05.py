import cv2
import sys

def limpa_borda_sup(img, width:int, height:int):
    p = [0,0]
    for j in range(width):
        if img[0,j] == 255:
            p[0] = j
            p[1] = 0
            cv2.floodFill(img, None, p, 0)

def limpa_borda_inf(img, width:int, height:int):
    p = [0,0]
    for j in range(width):
        if img[height-1,j] == 255:
            p[0] = j
            p[1] = height-1
            cv2.floodFill(img, None, p, 0)

def limpa_borda_esq(img, width:int, height:int):
    p = [0,0]
    for i in range(height):
        if img[i,0] == 255:
            p[0] = 0
            p[1] = i
            cv2.floodFill(img, None, p, 0)

def limpa_borda_dir(img, width:int, height:int):
    p = [0,0]
    for i in range(height):
        if img[i,width-1] == 255:
            p[0] = width-1
            p[1] = i
            cv2.floodFill(img, None, p, 0)

def limpa_bordas(img, width:int, height:int):
    width = imagem.shape[0]
    height = imagem.shape[1]
    p = [0,0]

    limpa_borda_sup(img, width, height)
    limpa_borda_inf(img, width, height)
    limpa_borda_esq(img, width, height)
    limpa_borda_dir(img, width, height)

    return img
    
def contar_bolhas(img):
    img = img.copy()
    width = img.shape[0]
    height = img.shape[1]

    img = limpa_bordas(img, width, height)

    bolhas_s_furos = 0
    bolhas_c_furos = 0

    p = [0,0]
    cor_fundo = 255//2
    cv2.floodFill(img, None, p, cor_fundo)

    for i in range(width):
        for j in range(height):
            if img[i, j] == 0:
                bolhas_c_furos += 1
                p[0] = j
                p[1] = i
                cv2.floodFill(img, None, p, cor_fundo)
                if img[i, j-1] == 255:
                    p[0] = j
                    p[1] = i-1
                    cv2.floodFill(img, None, p, cor_fundo+75)

    for i in range(width):
        for j in range(height):
            if img[i, j] == 255:
                bolhas_s_furos += 1
                p[0] = j
                p[1] = i
                cv2.floodFill(img, None, p, cor_fundo-75)

    return img, bolhas_s_furos, bolhas_c_furos

imagem = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

if imagem is None:
    sys.exit(1)

print(f'Imagem carregada com dimensão {imagem.shape[0]} x {imagem.shape[1]}.')

img, bolhas_s_furos, bolhas_c_furos = contar_bolhas(imagem)

print(f'Bolhas sem furos: {bolhas_s_furos}')
print(f'Bolhas com furos: {bolhas_c_furos}')
print(f'Bolhas totais: {bolhas_s_furos + bolhas_c_furos}')

cv2.imshow('Contagem_de_bolhas.png', img)
cv2.waitKey()
cv2.destroyAllWindows()

#cv2.imwrite('../figs/img03.png', img)