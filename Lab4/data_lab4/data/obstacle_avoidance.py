import cv2
import numpy as np
import csv

# Carrega os parâmetros de calibração
cv_file = cv2.FileStorage("./data/params_py_jorge.xml", cv2.FILE_STORAGE_READ)
Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
cv_file.release()

# Carrega os parâmetros de estimativa de profundidade
cv_file = cv2.FileStorage("./data/depth_estmation_params_py_teste_jorge.xml", cv2.FILE_STORAGE_READ)
numDisparities = int(cv_file.getNode("numDisparities").real())
blockSize = int(cv_file.getNode("blockSize").real())
M = cv_file.getNode("M").real()
cv_file.release()

# Inicializa as câmeras estéreo
left_camera = cv2.VideoCapture(0)
right_camera = cv2.VideoCapture(2)

if not left_camera.isOpened() or not right_camera.isOpened():
    print("Erro ao abrir as câmeras.")
    exit()

# Define as propriedades do vídeo de saída
frame_width = int(left_camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(left_camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_depth.avi', fourcc, 20.0, (frame_width, frame_height))

# Cria o objeto StereoBM para cálculo do mapa de disparidade
stereo = cv2.StereoBM_create(numDisparities=numDisparities, blockSize=blockSize)

# Inicializa a lista para armazenar as medições
measurements = []

while True:
    # Captura os quadros das câmeras
    retL, frameL = left_camera.read()
    retR, frameR = right_camera.read()

    if not retL or not retR:
        print("Erro ao capturar os quadros.")
        break

    # Aplica a retificação
    frameL_rectified = cv2.remap(frameL, Left_Stereo_Map_x, Left_Stereo_Map_y, cv2.INTER_LINEAR)
    frameR_rectified = cv2.remap(frameR, Right_Stereo_Map_x, Right_Stereo_Map_y, cv2.INTER_LINEAR)

    # Converte para escala de cinza
    grayL = cv2.cvtColor(frameL_rectified, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(frameR_rectified, cv2.COLOR_BGR2GRAY)

    # Calcula o mapa de disparidade
    disparity = stereo.compute(grayL, grayR)

    # Normaliza o mapa de disparidade para visualização
    disp_norm = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disp_norm = np.uint8(disp_norm)

    # Calcula o mapa de profundidade
    depth_map = M / (disparity + 1e-5)

    # Aplica um limiar para detectar objetos próximos
    depth_thresh = 100.0
    mask = cv2.inRange(depth_map, 10, depth_thresh)

    # Detecta contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)

    if cnts:
        # Obtém o maior contorno
        x, y, w, h = cv2.boundingRect(cnts[0])

        # Calcula a profundidade média da região
        mask2 = np.zeros_like(mask)
        cv2.drawContours(mask2, cnts, 0, (255), -1)
        depth_mean = cv2.mean(depth_map, mask=mask2)[0]

        # Exibe a profundidade média na imagem
        cv2.putText(frameL_rectified, f"Distancia: {depth_mean:.2f} cm", (x + 5, y - 40), 1, 2, (0, 0, 255), 2, 2)

        # Adiciona a medição à lista
        measurements.append([x, y, w, h, depth_mean])

    # Exibe a imagem com as medições
    cv2.imshow('Mapa de Profundidade', frameL_rectified)

    # Grava o vídeo
    out.write(frameL_rectified)

    # Ação para salvar as medições
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        with open('measurements.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['X', 'Y', 'Largura', 'Altura', 'Distancia (cm)'])
            writer.writerows(measurements)
        print("Medições salvas em 'measurements.csv'.")

    # Ação para sair
    if key == ord('q'):
        break

# Libera os recursos
left_camera.release()
right_camera.release()
out.release()
cv2.destroyAllWindows()
