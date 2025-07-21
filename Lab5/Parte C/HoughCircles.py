import cv2
import numpy as np

# Carrega a imagem em modo colorido
img = cv2.imread('igreja.jpeg', cv2.IMREAD_COLOR)

# Converte a imagem para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplica um desfoque para reduzir ruídos antes da detecção de círculos
img_blur = cv2.medianBlur(gray, 5)

# Aplica a Transformada de Hough para detecção de círculos
# Parâmetros:
# - Método: cv2.HOUGH_GRADIENT
# - dp: resolução do acumulador em relação à imagem
# - minDist: distância mínima entre os centros dos círculos detectados
# - param1: limiar superior para o detector de bordas Canny
# - param2: limiar para o acumulador do centro do círculo
# - minRadius e maxRadius: raio mínimo e máximo dos círculos a serem detectados
circles = cv2.HoughCircles(
    img_blur,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=img.shape[0] / 64,
    param1=300,
    param2=10,
    minRadius=90,
    maxRadius=95
)

# Se círculos forem detectados
if circles is not None:
    # Arredonda os valores e converte para inteiros
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # Desenha o círculo externo (verde)
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # Desenha o centro do círculo (vermelho)
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

# Exibe a imagem com os círculos detectados
cv2.imshow("Detected Circles", img)

# Salva a imagem com os círculos desenhados
cv2.imwrite("saida_circulos-igreja.jpg", img)
print("Imagem com círculos salva como 'saida_circulos.jpg'.")

# Aguarda uma tecla e fecha a janela
cv2.waitKey(0)
cv2.destroyAllWindows()

