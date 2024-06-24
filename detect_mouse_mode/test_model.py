import cv2
import mediapipe as mp
import time
import joblib
import numpy as np

MOUSE_DOWN_THRESHOLD = 0.045
model = joblib.load('notebooks/mouse_mode_detection/model-v9.joblib')
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


def get_index_thumb_tips(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global positions, mouse_down
    if result.hand_landmarks:
        landmark_data = []

        for landmark in result.hand_landmarks[0]:
            landmark_data.append(float(landmark.x))
            landmark_data.append(float(landmark.y))
            landmark_data.append(float(landmark.z))

        positions = landmark_data

        index_world = np.array([
            result.hand_landmarks[0][8].x,
            result.hand_landmarks[0][8].y,
            result.hand_landmarks[0][8].z
        ])

        thumb_world = np.array([
            result.hand_landmarks[0][4].x,
            result.hand_landmarks[0][4].y,
            result.hand_landmarks[0][4].z
        ])

        mouse_down = float(np.linalg.norm(index_world - thumb_world)) < MOUSE_DOWN_THRESHOLD


positions = None
mouse_down = False

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='detect_mouse_mode/hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=get_index_thumb_tips
)

with HandLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        height, width = frame.shape[:2]
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        landmarker.detect_async(mp_image, round(time.time() * 1000))

        if positions:
            prediction = model.predict([positions])
            prediction = prediction[0]

            if prediction == 0:
                cv2.putText(
                    frame,
                    'Mouse Mode OFF',
                    (50, 50),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA
                )
            else:
                cv2.putText(
                    frame,
                    'Mouse Mode ON',
                    (50, 50),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )
                if mouse_down:
                    cv2.putText(
                        frame,
                        'Mouse Down',
                        (50, 100),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA
                    )

            for idx in range(0, 21 * 3, 3):
                cv2.circle(
                    frame,
                    (int(positions[idx] * width), int(positions[idx + 1] * height)),
                    2,
                    (0, 0, 255),
                    2,
                )

        cv2.imshow('Mouse mode detection', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
