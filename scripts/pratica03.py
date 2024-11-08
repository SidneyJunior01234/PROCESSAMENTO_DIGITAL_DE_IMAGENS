import cv2
import numpy as np
import yaml
import matplotlib.pyplot as plt

# Configurações da senoide e do arquivo
SIDE = 256
PERIODOS = 4
AMPLITUDE = 127
ARQ_NOME_YML = f'senoide-{SIDE}.yml'
ARQ_NOME_PNG = f'senoide-{SIDE}.png'
GRAFICO = '../imagens/diferenca.png'

# 1. Criar a imagem senoide
imagem = np.zeros((SIDE, SIDE), dtype=np.float32)
for linha in range(SIDE):
    for coluna in range(SIDE):
        imagem[linha, coluna] = AMPLITUDE * np.sin(2 * np.pi * PERIODOS * coluna / SIDE) + 128

# 2. Salvar a imagem em formato YML
with open(ARQ_NOME_YML, 'w') as f:
    yaml.dump({'mat': imagem.tolist()}, f)

# 3. Ler a imagem do arquivo YML
with open(ARQ_NOME_YML, 'r') as f:
    data_yml = yaml.safe_load(f)
data_yml = np.asarray(data_yml['mat'], dtype=np.float32)

# 4. Normalizar e salvar a imagem em formato PNG
cv2.normalize(data_yml, data_yml, 0, 255, cv2.NORM_MINMAX)
data_png = data_yml.astype(np.uint8)
cv2.imwrite(ARQ_NOME_PNG, data_png)

# 5. Ler a imagem salva em PNG
data_png = cv2.imread(ARQ_NOME_PNG, cv2.IMREAD_GRAYSCALE).astype(np.float32)

# 6. Selecionar uma linha para comparação
linha_escolhida = SIDE // 2  # linha central
linha_yml = data_yml[linha_escolhida, :]
linha_png = data_png[linha_escolhida, :]

# 7. Calcular a diferença entre as linhas
diferenca = linha_yml - linha_png

# 8. Plotar o gráfico da diferença
plt.figure(figsize=(10, 5))
plt.plot(diferenca, label='Diferença (YML - PNG)', color='red')
plt.title('Diferença entre as linhas extraídas das imagens YML e PNG')
plt.xlabel('Coluna')
plt.ylabel('Diferença de valores de pixel')
plt.legend()
plt.grid(True)
plt.savefig(GRAFICO)
plt.show()