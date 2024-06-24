from cv2 import VideoCapture, flip, imshow, circle, destroyWindow, getWindowProperty, waitKey
import mediapipe as mp
import pyautogui
from model.utils.average import Average
from model.utils.mouse_behaviour import MouseBehaviour
from time import time
import dearpygui.dearpygui as dpg
import joblib
from functools import reduce


class ModelHandler:
    def __init__(self):
        # mediapipe settings
        self.BaseOptions = mp.tasks.BaseOptions
        self.HandLandmarker = mp.tasks.vision.HandLandmarker
        self.HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        self.HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.options = self.HandLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path='gui/utils/hand_landmarker.task'), # utils/hand_landmarker.task
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.callback
        )
        self.hands = self.HandLandmarker.create_from_options(self.options)

        # pyautogui settings
        pyautogui.FAILSAFE = False

        # instantiation of required classes and functions
        self.cap = VideoCapture(0)
        self.avg = Average(lim=15)
        self.mouse_behaviour = MouseBehaviour()
        self.mulx = 4.5
        self.muly = 5.5
        
        # instantiate mouse mode models
        self.mouse_mode_model = joblib.load('gui/utils/model.joblib')
        self.last_hand_landmarks = None
    
    def callback(self, results, _, __):
        if results.hand_landmarks:
            self.last_hand_landmarks = reduce(lambda x, y: x + y, [[i.x, i.y, i.z] for i in results.hand_landmarks[0]])
            
            is_mouse_mode = self.mouse_mode_model.predict([self.last_hand_landmarks])[0]
            if is_mouse_mode == 0:
                return
            
            cursor = (
                sum(i.x for idx, i in enumerate(results.hand_landmarks[0]) if idx not in [4, 8]) / 19,
                sum(i.y for idx, i in enumerate(results.hand_landmarks[0]) if idx not in [4, 8]) / 19,
            )
            
            cursor = self.avg.get(cursor[0], cursor[1])
            
            self.mouse_behaviour.detect(
                cursor,
                [results.hand_landmarks[0][8].x, results.hand_landmarks[0][8].y, results.hand_landmarks[0][8].z],
                [results.hand_landmarks[0][4].x, results.hand_landmarks[0][4].y, results.hand_landmarks[0][4].z],
                self.mulx,
                self.muly,
            )
        else:
            self.last_hand_landmarks = None
    
    def set_multiplier(self, mulx, muly):
        self.mulx = mulx
        self.muly = muly

    def run_main_program(self):
        if not dpg.get_value('start_detection'):
            try:
                if self.cap.isOpened():
                    if getWindowProperty('Webcam View', 0) >= 0:
                        destroyWindow('Webcam View')
            except:
                return
            
            return
        
        if self.hands and self.cap.isOpened():
            success, image = self.cap.read()
            height, width = image.shape[:2]
            if not success:
                print("Ignoring empty camera frame.")
                return
            
            image = flip(image, 1)
            
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            self.hands.detect_async(mp_image, round(time() * 1000))
                          
            # cursor
            if self.mouse_behaviour.cursor is not None:
                circle(
                    image, 
                    (int(self.mouse_behaviour.cursor[0] * width), 
                    int(self.mouse_behaviour.cursor[1] * height)), 
                    3, (255, 0, 255), 2
                )
                        
            # center
            circle(
                image, 
                (int(self.mouse_behaviour.center[0] * width), 
                int(self.mouse_behaviour.center[1] * height)), 
                3, (0, 0, 255), 2
            )
            
            if dpg.get_value('show_camera'):
                imshow('Webcam View', image)
                waitKey(1)
            else:
                try:
                    if getWindowProperty('Webcam View', 0) >= 0:
                        destroyWindow('Webcam View')
                except:
                    pass
                
    def release_resources(self):
        self.cap.release()
