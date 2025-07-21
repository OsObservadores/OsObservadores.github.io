import cv2
import numpy as np

# Leitura da imagem
img = cv2.imread('placa.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detecção de bordas
edges = cv2.Canny(gray, 50, 200)

# Parâmetros do Hough
max_slider = 70  # Aumenta para reduzir o número de linhas
min_length = 50   # Tamanho mínimo da linha

# Detecta linhas
lines = cv2.HoughLinesP(edges, 1, np.pi/180, max_slider, minLineLength=10, maxLineGap=250)

# Desenha linhas com filtro e transparência
if lines is not None:
    overlay = img.copy()
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if length >= min_length:
            cv2.line(overlay, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)

# Exibe e salva o resultado
cv2.imshow("Result Image", img)
cv2.imwrite("saida_linhas_.jpg", img)
print("Imagem salva como 'saida_linhas.jpg'")
cv2.waitKey(0)
cv2.destroyAllWindows()


