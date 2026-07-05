# core/hand_tracker.py
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from core.config import Config

class HandTracker:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path=Config.MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def get_landmarks(self, frame):
        """Processes the frame and returns hand landmarks if found."""
        # Convert BGR (OpenCV default) to RGB (MediaPipe requirement)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect hands
        result = self.detector.detect(mp_image)
        
        # Return the first hand found, otherwise None
        if result.hand_landmarks:
            return result.hand_landmarks[0]
        return None