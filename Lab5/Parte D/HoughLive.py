import threading
import time
import numpy as np
import cv2 as cv

class CameraThread(threading.Thread):
    def __init__(self, cam_id):
        super().__init__()
        self.cap = cv.VideoCapture(cam_id)
        self.ret = False
        self.frame = None
        self.running = True
        self.lock = threading.Lock()

        # Aquecimento da câmera
        for _ in range(10):
            ret, frame = self.cap.read()
            if ret:
                break
            time.sleep(0.1)

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret
                if ret:
                    self.frame = frame
            time.sleep(0.001)

    def get_frame(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.cap.release()

# IDs das câmeras
CamL_id = 2
CamR_id = 0

camL_thread = CameraThread(CamL_id)
camR_thread = CameraThread(CamR_id)

camL_thread.start()
camR_thread.start()

# Parâmetros de vídeo
fps = 10.0
height = int(camL_thread.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
outm = cv.VideoWriter('HoughVideo.mp4', cv.VideoWriter_fourcc(*'mp4v'), fps, (1280, height))

def process_hough(frame):
    output = frame.copy()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Detecção de círculos
    blur = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, dp=1, minDist=gray.shape[0] / 64,
                              param1=300, param2=10, minRadius=90, maxRadius=95)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Círculo
            cv.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)     # Centro
    
    # Detecção de linhas
    edges = cv.Canny(gray, 50, 200)
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 70, minLineLength=50, maxLineGap=250)
    if lines is not None:
        overlay = output.copy()
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if length >= 50:
                cv.line(overlay, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv.addWeighted(overlay, 0.4, output, 0.6, 0, output)
    
    return output

try:
    while True:
        retL, frameL = camL_thread.get_frame()
        retR, frameR = camR_thread.get_frame()

        if not retL or not retR:
            time.sleep(0.01)
            continue

        processedL = process_hough(frameL)
        processedR = process_hough(frameR)

        # Combina os dois frames lado a lado
        combined = np.hstack((processedL, processedR))

        print(f"combined shape: {combined.shape}")
        outm.write(combined)
        cv.imshow("Hough Circle + Line Real-Time", combined)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camL_thread.stop()
    camR_thread.stop()
    cv.destroyAllWindows()
    outm.release()

