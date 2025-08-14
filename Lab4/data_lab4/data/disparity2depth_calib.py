import cv2
import numpy as np

# --- 1. Lê os parâmetros de calibração estéreo ---
cv_file = cv2.FileStorage("./data/params_py.xml", cv2.FILE_STORAGE_READ)
Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
cv_file.release()

# --- 2. Lê o mapa de disparidade já salvo ---
cv_file = cv2.FileStorage("./data/depth_estmation_params_py.xml", cv2.FILE_STORAGE_READ)
disparity = cv_file.getNode("disparity").mat()
cv_file.release()

# --- 3. Amostras de calibração prática (Exemplo real) ---
# Substitua pelos seus valores medidos na prática
# Exemplo: [(disparity, depth_in_cm), ...]
samples = [
    (30.5, 100),  # objeto a 1m
    (21.0, 150),  # objeto a 1.5m
    (15.0, 200),  # objeto a 2m
    (12.0, 250),  # objeto a 2.5m
]

# --- 4. Prepara os dados para resolver: depth = M0*(1/disparity) + M1 ---
N = len(samples)
coeff = np.zeros((N, 2), dtype=np.float32)
z = np.zeros((N, 1), dtype=np.float32)

for i, (disp, depth) in enumerate(samples):
    coeff[i, 0] = 1.0 / disp
    coeff[i, 1] = 1.0
    z[i, 0] = depth

# --- 5. Resolve para M ---
ret, M = cv2.solve(coeff, z, flags=cv2.DECOMP_QR)
M0, M1 = M[0, 0], M[1, 0]
print(f"Coeficientes calibrados: M0 = {M0:.4f}, M1 = {M1:.4f}")

# --- 6. Calcula o mapa de profundidade real ---
# Evita divisões por zero ou valores negativos
disp_safe = np.copy(disparity)
disp_safe[disp_safe <= 0.0] = np.nan  # ignora valores inválidos

# Aplica a equação depth = M0*(1/disp) + M1
depth_map = M0 * (1.0 / disp_safe) + M1

# --- 7. Salva o mapa de profundidade real no mesmo XML ---
fs_write = cv2.FileStorage("./data/depth_estmation_params_py_2.xml", cv2.FILE_STORAGE_APPEND)
fs_write.write("depth", depth_map)
fs_write.release()
print("✅ Mapa de profundidade salvo em depth_estmation_params_py.xml")
