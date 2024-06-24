import cv2
import mediapipe as mp
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

positions = []


def get_index_thumb_tips(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    if result.hand_landmarks:
        landmark_data = []

        for landmark in result.hand_landmarks[0]:
            landmark_data.append(float(landmark.x))
            landmark_data.append(float(landmark.y))
            landmark_data.append(float(landmark.z))

        positions.append(landmark_data)


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
        
        frame = cv2.flip(frame, 1)
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        landmarker.detect_async(mp_image, round(time.time() * 1000))

        if positions:
            arr = positions[-1]
            for idx in range(0, 21 * 3, 3):
                cv2.circle(
                    frame,
                    # arr[idx:idx+2],
                    (int(arr[idx] * width), int(arr[idx + 1] * height)),
                    2,
                    (0, 0, 255),
                    2,
                )

        cv2.imshow('Mouse mode detection', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

with open(f'notebooks/mouse_mode_detection/mouse_mode/mouse_mode_on_{str(time.time())}.csv', 'a') as file:
    data_points = positions
    data = ""
    for d in data_points:
        data += ", ".join([str(i) for i in d]) + "\n"
    file.write(data)
