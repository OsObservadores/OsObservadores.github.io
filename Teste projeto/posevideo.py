import cv2
import mediapipe as mp
import numpy as np
import math

def calculate_angle(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)
    ba, bc = a - b, c - b
    ba_norm, bc_norm = np.linalg.norm(ba), np.linalg.norm(bc)
    if ba_norm == 0 or bc_norm == 0:
        return 180.0
    cos_ang = np.dot(ba, bc) / (ba_norm * bc_norm)
    cos_ang = np.clip(cos_ang, -1.0, 1.0)
    return math.degrees(math.acos(cos_ang))

def classify_pose(landmarks):
    xs = [lm.x for lm in landmarks]
    ys = [lm.y for lm in landmarks]
    width, height = max(xs) - min(xs), max(ys) - min(ys)
    if width > height * 1.3:
        return 'Deitada'
    mp_pose = mp.solutions.pose
    left_hip   = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,  landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee  = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    right_hip   = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,  landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    right_knee  = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    left_angle  = calculate_angle(left_hip, left_knee, left_ankle)
    right_angle = calculate_angle(right_hip, right_knee, right_ankle)
    if (left_angle + right_angle) / 2.0 < 160:
        return 'Sentada'
    return 'Em pé'

def main():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError('Não foi possível acessar a webcam.')
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print('Falha ao capturar frame da webcam.')
                break
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            annotated = frame.copy()
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    annotated, results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style()
                )
                label = classify_pose(results.pose_landmarks.landmark)
                # sobrepõe o rótulo
                font, pos, scale, thickness = cv2.FONT_HERSHEY_SIMPLEX, (20,30), 1.0, 2
                cv2.putText(annotated, label, pos, font, scale, (0,0,0), thickness+2, cv2.LINE_AA)
                cv2.putText(annotated, label, pos, font, scale, (255,255,255), thickness, cv2.LINE_AA)
            cv2.imshow('Pose Detection (press q to quit)', annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        pose.close()

if __name__ == '__main__':
    main()