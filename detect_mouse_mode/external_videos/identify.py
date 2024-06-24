import cv2
import mediapipe as mp
import time
from utils import draw_landmarks_on_image


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

positions = []


def get_finger_tips(result: HandLandmarkerResult):
    if result.hand_landmarks:
        landmark_data = []

        for landmark in result.hand_landmarks[0]:
            landmark_data.append(float(landmark.x))
            landmark_data.append(float(landmark.y))
            landmark_data.append(float(landmark.z))

        positions.append(landmark_data)


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='detect_mouse_mode/hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO,
)

with HandLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture("WIN_20240527_14_42_17_Pro.mp4")

    while True:
        _, frame = cap.read()
        if frame is None:
            break

        height, width = frame.shape[:2]
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        results = landmarker.detect_for_video(mp_image, round(time.time() * 1000))

        if results:
            get_finger_tips(results)

        image = draw_landmarks_on_image(mp_image.numpy_view(), results)

        cv2.imshow('Mouse mode detection', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

with open(f'mouse_mode_on_{str(time.time())}.csv', 'a') as file:
    data_points = positions
    data = ""
    for d in data_points:
        data += ", ".join([str(i) for i in d]) + "\n"
    file.write(data)
