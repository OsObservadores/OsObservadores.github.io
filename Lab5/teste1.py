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

        for _ in range(10):  # aquecimento da câmera
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


CamL_id = 2
CamR_id = 0

camL_thread = CameraThread(CamL_id)
camR_thread = CameraThread(CamR_id)

camL_thread.start()
camR_thread.start()

# Inicializa o SIFT e FLANN
sift = cv.SIFT_create()
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)

MIN_MATCH_COUNT = 10

try:
    while True:
        retL, frameL = camL_thread.get_frame()
        retR, frameR = camR_thread.get_frame()

        if not retL or not retR:
            time.sleep(0.01)
            continue

        # Converte para escala de cinza
        grayL = cv.cvtColor(frameL, cv.COLOR_BGR2GRAY)
        grayR = cv.cvtColor(frameR, cv.COLOR_BGR2GRAY)

        # Detecta keypoints e descritores
        kp1, des1 = sift.detectAndCompute(grayL, None)
        kp2, des2 = sift.detectAndCompute(grayR, None)

        if des1 is None or des2 is None:
            continue

        # Match com FLANN
        matches = flann.knnMatch(des1, des2, k=2)

        # Lowe’s ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        matchesMask = None

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
        else:
            matchesMask = None

        # Desenhar os matches
        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=None,
                           matchesMask=matchesMask,
                           flags=2)

        matched_img = cv.drawMatches(grayL, kp1, grayR, kp2, good, None, **draw_params)

        cv.imshow("Feature Matching Real-Time", matched_img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camL_thread.stop()
    camR_thread.stop()
    cv.destroyAllWindows()
