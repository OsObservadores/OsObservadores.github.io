import threading
import time
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

class CameraThread(threading.Thread):
    def __init__(self, cam_id):
        super().__init__()
        self.cap = cv.VideoCapture(cam_id)
        self.ret = False
        self.frame = None
        self.running = True
        self.lock = threading.Lock()

        # Tentativa de "aquecimento" da câmera
        for _ in range(10):
            ret, frame = self.cap.read()
            if ret:
                break
            time.sleep(0.1)  # espera 100ms

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret
                if ret:
                    self.frame = ('frame', cv.IMREAD_GRAYSCALE)
            time.sleep(0.001)

    def get_frame(self):
        with self.lock:
            return self.ret, self.frame

    def stop(self):
        self.running = False
        self.cap.release()

CamL_id = 2
CamR_id = 0

camL_thread = CameraThread(CamL_id)
camR_thread = CameraThread(CamR_id)

camL_thread.start()
camR_thread.start()

fps = 60.0
width = int(camL_thread.cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(camL_thread.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'XVID')
outL = cv.VideoWriter('saidaL.avi', fourcc, fps, (width, height))
outR = cv.VideoWriter('saidaR.avi', fourcc, fps, (width, height))

try:
    while True:
        retL, frameL = camL_thread.get_frame()
        retR, frameR = camR_thread.get_frame()

        # Vamos ignorar falhas temporárias (esperar até ambos os frames estarem prontos)
        if not retL or not retR:
            time.sleep(0.01)
            continue

        outL.write(frameL)
        outR.write(frameR)

        cv.imshow('Camera Esquerda', frameL)
        cv.imshow('Camera Direita', frameR)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camL_thread.stop()
    camR_thread.stop()
    outL.release()
    outR.release()
    cv.destroyAllWindows()
