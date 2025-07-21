import numpy as np
import cv2
import time
import os

# Cria os diretórios se não existirem
os.makedirs('./data/stereo1', exist_ok=True)
os.makedirs('./data/stereo2', exist_ok=True)

print("Checking the right and left camera IDs:")
print("Press (y) if IDs are correct and (n) to swap the IDs")
print("Press enter to start the process >> ")
input()

# Check for left and right camera IDs
CamL_id = 2
CamR_id = 0

CamL= cv2.VideoCapture(CamL_id)
CamR= cv2.VideoCapture(CamR_id)

for i in range(100):
    retL, frameL= CamL.read()
    retR, frameR= CamR.read()

cv2.imshow('imgL',frameL)
cv2.imshow('imgR',frameR)

if cv2.waitKey(0) & 0xFF == ord('y') or cv2.waitKey(0) & 0xFF == ord('Y'):
    CamL_id = 2
    CamR_id = 0
    print("Camera IDs maintained")

elif cv2.waitKey(0) & 0xFF == ord('n') or cv2.waitKey(0) & 0xFF == ord('N'):
    CamL_id = 0
    CamR_id = 2
    print("Camera IDs swapped")
else:
    print("Wrong input response")
    exit(-1)
CamR.release()
CamL.release()

CamL= cv2.VideoCapture(CamL_id)
CamR= cv2.VideoCapture(CamR_id)
output_path = "./data/"

start = time.time()
T = 10
count = 0

while True:
    retR, frameR = CamR.read()
    retL, frameL = CamL.read()
    
    if not retL or not retR:
        print("Erro ao capturar imagens das câmeras.")
        break

    # Exibe as imagens
    cv2.imshow('imgR', frameR)
    cv2.imshow('imgL', frameL)

    # Converte para tons de cinza
    grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
    grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)

    # Procura o padrão de tabuleiro 9x6
    retR_corners, cornersR = cv2.findChessboardCorners(grayR, (8, 6), None)
    retL_corners, cornersL = cv2.findChessboardCorners(grayL, (8, 6), None)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # Tecla ESC
        print("Encerrando a captura.")
        break

    elif key == 32:  # Tecla espaço (ASCII 32)
        if retR_corners and retL_corners:
            count += 1
            cv2.imwrite(output_path + f'stereo1/imgteste.png', frameR)
            cv2.imwrite(output_path + f'stereo2/imgteste.png', frameL)
            print(f"Imagem {count} salva com sucesso!")
        else:
            print("Tabuleiro de xadrez não detectado em ambas as imagens.")


# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()
