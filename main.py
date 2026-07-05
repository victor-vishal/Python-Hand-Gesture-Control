import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui
import math
import time
import numpy as np

# --- CONFIGURATION ---
class Config:
    MODEL_PATH = 'hand_landmarker.task'
    SENSITIVITY = 3.5      
    SMOOTHING = 5          
    CLICK_THRESHOLD = 0.05 
    CLICK_COOLDOWN = 0.3   # Re-added your cooldown to prevent spam clicking

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
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self.detector.detect(mp_image)
        
        if result.hand_landmarks:
            return result.hand_landmarks[0]
        return None

class MouseController:
    def __init__(self):
        pyautogui.PAUSE = 0
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = self.screen_w // 2, self.screen_h // 2
        self.last_click_time = 0

    def move_cursor(self, index_landmark):
        """Calculates sensitivity, smoothing, and moves the physical mouse."""
        # 1. Sensitivity Math
        offset_x = (index_landmark.x - 0.5) * Config.SENSITIVITY
        offset_y = (index_landmark.y - 0.5) * Config.SENSITIVITY
        target_x = (0.5 + offset_x) * self.screen_w
        target_y = (0.5 + offset_y) * self.screen_h

        # 2. Smoothing
        curr_x = self.prev_x + (target_x - self.prev_x) / Config.SMOOTHING
        curr_y = self.prev_y + (target_y - self.prev_y) / Config.SMOOTHING
        
        # 3. Clamping & Execution
        final_x = np.clip(curr_x, 0, self.screen_w)
        final_y = np.clip(curr_y, 0, self.screen_h)
        pyautogui.moveTo(final_x, final_y)
        
        # Update previous positions
        self.prev_x, self.prev_y = final_x, final_y

    def check_click(self, index, thumb, frame, w, h):
        """Calculates distance and triggers click with a cooldown."""
        dist = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2)
        current_time = time.time()

        if dist < Config.CLICK_THRESHOLD:
            cv2.circle(frame, (int(index.x * w), int(index.y * h)), 15, (0, 0, 255), -1)
            # Apply Cooldown
            if current_time - self.last_click_time > Config.CLICK_COOLDOWN:
                pyautogui.click()
                self.last_click_time = current_time
        else:
            cv2.circle(frame, (int(index.x * w), int(index.y * h)), 10, (0, 255, 0), -1)

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    mouse = MouseController()
    
    # FPS Tracking
    prev_time = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
        prev_time = curr_time
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Process Hand
        landmarks = tracker.get_landmarks(frame)

        if landmarks:
            index = landmarks[8]
            thumb = landmarks[4]
            
            # Execute Controls
            mouse.move_cursor(index)
            mouse.check_click(index, thumb, frame, w, h)

        cv2.imshow('python-hand-gesture-control', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()