import cv2
import numpy as np
import sys

ALTURA_MAX_SLIDER = 100
DECAI_MAX_SLIDER = 20
CENTRO_MAX_SLIDER = 100
DESC_QUADROS = 10

def aplicar_tilt_shift(frame, altura_foco, decaimento, centro):
    altura_imagem, largura_imagem = frame.shape[:2]
    centro_y = int(altura_imagem * centro)
    altura_foco_px = int(altura_imagem * altura_foco)

    mascara = np.zeros((altura_imagem, largura_imagem), dtype=np.float32)
    mascara[max(0, centro_y - altura_foco_px // 2):min(altura_imagem, centro_y + altura_foco_px // 2), :] = 1

    if decaimento < 1:
        decaimento = 1
    elif decaimento % 2 == 0:
        decaimento += 1

    mascara = cv2.GaussianBlur(mascara, (decaimento, decaimento), sigmaX=decaimento, sigmaY=decaimento)

    frame_borrado = cv2.GaussianBlur(frame, (21, 21), 0)
    resultado = (frame * mascara[..., np.newaxis] + frame_borrado * (1 - mascara[..., np.newaxis])).astype(np.uint8)

    return resultado

def processar_video(input_video_path, output_video_path, altura_foco, decaimento, centro):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (largura, altura))

    contador = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if contador >= DESC_QUADROS:
            contador = 0
            quadro_tiltshift = aplicar_tilt_shift(frame, altura_foco, decaimento, centro)
            out.write(quadro_tiltshift)
            cv2.imshow("Tilt-Shift", quadro_tiltshift)

        contador += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Vídeo processado salvo como '{output_video_path}'.")

def ajustar_parametros(imagem_path):
    imagem = cv2.imread(imagem_path)
    if imagem is None:
        print("Erro ao abrir a imagem.")
        return None, None, None

    cv2.namedWindow("Ajustar Parâmetros")
    cv2.createTrackbar("Altura do Foco", "Ajustar Parâmetros", 50, ALTURA_MAX_SLIDER, lambda x: None)
    cv2.createTrackbar("Decaimento do Desfoque", "Ajustar Parâmetros", 10, DECAI_MAX_SLIDER, lambda x: None)
    cv2.createTrackbar("Centro Vertical", "Ajustar Parâmetros", 50, CENTRO_MAX_SLIDER, lambda x: None)

    while True:
        altura_foco = cv2.getTrackbarPos("Altura do Foco", "Ajustar Parâmetros") / ALTURA_MAX_SLIDER
        decaimento = cv2.getTrackbarPos("Decaimento do Desfoque", "Ajustar Parâmetros")
        centro = cv2.getTrackbarPos("Centro Vertical", "Ajustar Parâmetros") / CENTRO_MAX_SLIDER

        imagem_tiltshift = aplicar_tilt_shift(imagem, altura_foco, decaimento, centro)

        cv2.imshow("Ajustar Parâmetros", imagem_tiltshift)

        # Pressione 's' para salvar os parâmetros e sair
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    cv2.destroyAllWindows()
    return altura_foco, decaimento, centro

if __name__ == "__main__":
    imagem_path = sys.argv[1]
    input_video = sys.argv[2]
    output_video = "tiltshift_video.mp4"

    altura_foco, decaimento, centro = ajustar_parametros(imagem_path)

    if altura_foco is not None and decaimento is not None and centro is not None:
        processar_video(input_video, output_video, altura_foco, decaimento, centro)
