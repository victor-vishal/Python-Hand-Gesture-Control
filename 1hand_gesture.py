import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui
import math
import time
import numpy as np

# --- CONFIGURATION ---
MODEL_PATH = 'hand_landmarker.task'
SENSITIVITY = 3.5      # Increase this (e.g., 2.0, 2.5) for more cursor travel
SMOOTHING = 5          # Higher = less jitter, more "weight"
CLICK_THRESHOLD = 0.05 
pyautogui.PAUSE = 0

# --- INITIALIZATION ---
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5, # Lowered to keep tracking even if hand is partially skewed
    min_hand_presence_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = screen_w // 2, screen_h // 2

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        landmarks = detection_result.hand_landmarks[0]
        index = landmarks[8]
        thumb = landmarks[4]

        # 1. HIGH SENSITIVITY CALCULATION
        # Find the center of the camera (0.5, 0.5)
        # Calculate how far the finger is from center and multiply it
        offset_x = (index.x - 0.5) * SENSITIVITY
        offset_y = (index.y - 0.5) * SENSITIVITY

        # Map that offset back to screen coordinates
        target_x = (0.5 + offset_x) * screen_w
        target_y = (0.5 + offset_y) * screen_h

        # 2. SMOOTHING
        curr_x = prev_x + (target_x - prev_x) / SMOOTHING
        curr_y = prev_y + (target_y - prev_y) / SMOOTHING
        
        # 3. CLAMPING & MOVEMENT
        # Ensure values stay within actual screen pixel bounds
        final_x = np.clip(curr_x, 0, screen_w)
        final_y = np.clip(curr_y, 0, screen_h)
        
        pyautogui.moveTo(final_x, final_y)
        prev_x, prev_y = final_x, final_y

        # 4. CLICK LOGIC
        dist = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2)
        if dist < CLICK_THRESHOLD:
            cv2.circle(frame, (int(index.x*w), int(index.y*h)), 15, (0, 0, 255), -1)
            pyautogui.click()
        else:
            cv2.circle(frame, (int(index.x*w), int(index.y*h)), 10, (0, 255, 0), -1)

    cv2.imshow('High Sensitivity Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()











# import cv2
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# import pyautogui
# import math
# import time
# import numpy as np

# # --- CONFIGURATION ---
# MODEL_PATH = 'hand_landmarker.task'
# # Increase this value to make the "Pink Box" smaller and the mouse MORE sensitive
# FRAME_REDUCTION = 150  
# SMOOTHING = 5         
# CLICK_THRESHOLD = 0.05 
# pyautogui.PAUSE = 0

# # --- INITIALIZATION ---
# base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
# options = vision.HandLandmarkerOptions(
#     base_options=base_options,
#     num_hands=1,
#     min_hand_detection_confidence=0.7,
#     min_hand_presence_confidence=0.7
# )
# detector = vision.HandLandmarker.create_from_options(options)

# cap = cv2.VideoCapture(0)
# screen_w, screen_h = pyautogui.size()

# prev_x, prev_y = 0, 0
# last_click_time = 0

# while cap.isOpened():
#     success, frame = cap.read()
#     if not success: break

#     frame = cv2.flip(frame, 1)
#     h, w, _ = frame.shape
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

#     detection_result = detector.detect(mp_image)

#     if detection_result.hand_landmarks:
#         landmarks = detection_result.hand_landmarks[0]
#         index = landmarks[8]
#         thumb = landmarks[4]

#         # 1. GET RAW PIXEL COORDINATES
#         ix, iy = index.x * w, index.y * h

#         # 2. THE SENSITIVITY MATH (Mapping & Clamping)
#         # We map the inner "Active Zone" to the full screen resolution
#         # np.interp handles the scaling, and we clamp the values to screen boundaries
#         target_x = np.interp(ix, (FRAME_REDUCTION, w - FRAME_REDUCTION), (0, screen_w))
#         target_y = np.interp(iy, (FRAME_REDUCTION, h - FRAME_REDUCTION), (0, screen_h))

#         # 3. SMOOTHING (Ensures the cursor doesn't jitter)
#         curr_x = prev_x + (target_x - prev_x) / SMOOTHING
#         curr_y = prev_y + (target_y - prev_y) / SMOOTHING
        
#         # Move mouse (clamped to screen size to prevent errors)
#         pyautogui.moveTo(np.clip(curr_x, 0, screen_w), np.clip(curr_y, 0, screen_h))
#         prev_x, prev_y = curr_x, curr_y

#         # 4. CLICK LOGIC (Non-blocking)
#         dist = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2)
#         curr_time = time.time()
        
#         if dist < CLICK_THRESHOLD:
#             cv2.circle(frame, (int(ix), int(iy)), 15, (0, 0, 255), -1)
#             if curr_time - last_click_time > 0.3:
#                 pyautogui.click()
#                 last_click_time = curr_time
#         else:
#             cv2.circle(frame, (int(ix), int(iy)), 10, (0, 255, 0), -1)

#     # VISUAL GUIDE: Draw the "Active Zone"
#     # When your finger hits these lines, the cursor hits the edge of your monitor
#     cv2.rectangle(frame, (FRAME_REDUCTION, FRAME_REDUCTION), 
#                   (w - FRAME_REDUCTION, h - FRAME_REDUCTION), (255, 0, 255), 2)
    
#     cv2.putText(frame, "Active Tracking Zone", (FRAME_REDUCTION, FRAME_REDUCTION - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

#     cv2.imshow('Hand Controller - Corners Fixed', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()














# # import cv2
# # import mediapipe as mp
# # from mediapipe.tasks import python
# # from mediapipe.tasks.python import vision
# # import pyautogui
# # import math
# # import time
# # import numpy as np

# # # --- CONFIGURATION ---
# # MODEL_PATH = 'hand_landmarker.task'
# # FRAME_REDUCTION = 80  # Pixels to skip at camera edges (helps reach screen corners)
# # SMOOTHING = 4         # Higher = smoother but slower cursor
# # CLICK_THRESHOLD = 0.05 # Distance between thumb and index to trigger click
# # PYAUTOGUI_DELAY = 0   # Removes default delay for snappier feel

# # pyautogui.PAUSE = PYAUTOGUI_DELAY

# # # --- INITIALIZATION ---
# # base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
# # options = vision.HandLandmarkerOptions(
# #     base_options=base_options,
# #     num_hands=1,
# #     min_hand_detection_confidence=0.7,
# #     min_hand_presence_confidence=0.7
# # )
# # detector = vision.HandLandmarker.create_from_options(options)

# # cap = cv2.VideoCapture(0)
# # screen_w, screen_h = pyautogui.size()

# # # State variables
# # prev_x, prev_y = 0, 0
# # last_click_time = 0

# # print("Controller active. Press 'q' to quit.")

# # while cap.isOpened():
# #     success, frame = cap.read()
# #     if not success:
# #         break

# #     # Flip and process frame
# #     frame = cv2.flip(frame, 1)
# #     h, w, _ = frame.shape
# #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

# #     # Detect hand landmarks
# #     detection_result = detector.detect(mp_image)

# #     if detection_result.hand_landmarks:
# #         # Get the first hand detected
# #         landmarks = detection_result.hand_landmarks[0]
        
# #         # Landmark 8: Index Fingertip | Landmark 4: Thumb Tip
# #         index = landmarks[8]
# #         thumb = landmarks[4]
# #         middle = landmarks[12] # Optional: Middle fingertip for better click logic


# #         # 1. COORDINATE MAPPING
# #         # Convert normalized (0-1) to pixel values
# #         ix, iy = index.x * w, index.y * h

        
# #         # Map camera coordinates to screen coordinates with a "deadzone" buffer
# #         # This makes it much easier to reach the edges of your monitor
# #         target_x = np.interp(ix, (FRAME_REDUCTION, w - FRAME_REDUCTION), (0, screen_w))
# #         target_y = np.interp(iy, (FRAME_REDUCTION, h - FRAME_REDUCTION), (0, screen_h))

# #         # 2. SMOOTHING
# #         # Linear Interpolation: Current = Prev + (Target - Prev) / Smoothing
# #         curr_x = prev_x + (target_x - prev_x) / SMOOTHING
# #         curr_y = prev_y + (target_y - prev_y) / SMOOTHING
        
# #         # Move the physical mouse
# #         pyautogui.moveTo(curr_x, curr_y)
# #         prev_x, prev_y = curr_x, curr_y

# #         # 3. CLICK LOGIC
# #         # Calculate 3D Euclidean distance (MediaPipe provides z-axis too)
# #         dist = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2)
        
# #         curr_time = time.time()
# #         # Visual feedback: Draw circle on index finger
# #         if dist < CLICK_THRESHOLD:
# #             cv2.circle(frame, (int(ix), int(iy)), 15, (0, 0, 255), cv2.FILLED) # Red
# #             # Non-blocking click: only trigger if 0.3s has passed
# #             if curr_time - last_click_time > 0.3:
# #                 pyautogui.click()
# #                 last_click_time = curr_time
# #         else:
# #             cv2.circle(frame, (int(ix), int(iy)), 10, (0, 255, 0), cv2.FILLED) # Green

# #     # Draw the boundary box for visual reference (The Deadzone)
# #     cv2.rectangle(frame, (FRAME_REDUCTION, FRAME_REDUCTION), 
# #                   (w - FRAME_REDUCTION, h - FRAME_REDUCTION), (255, 0, 255), 2)

# #     cv2.imshow('AI Virtual Mouse', frame)
    
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()








# # # import cv2
# # # import mediapipe as mp
# # # from mediapipe.tasks import python
# # # from mediapipe.tasks.python import vision
# # # import pyautogui
# # # import math
# # # import time

# # # # Disable PyAutoGUI fail-safe (use with caution) or set a small pause
# # # pyautogui.PAUSE = 0 

# # # # 1. Setup MediaPipe
# # # base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
# # # options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
# # # detector = vision.HandLandmarker.create_from_options(options)

# # # cap = cv2.VideoCapture(0)
# # # screen_w, screen_h = pyautogui.size()

# # # # Configuration
# # # SMOOTHING = 5  # Increase for smoother, slower movement
# # # frame_reduction = 100 # Deadzone: ignore 100px from camera edges to reach screen corners easier
# # # last_click_time = 0
# # # prev_x, prev_y = 0, 0

# # # while cap.isOpened():
# # #     success, frame = cap.read()
# # #     if not success: break

# # #     frame = cv2.flip(frame, 1)
# # #     h, w, _ = frame.shape
# # #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# # #     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

# # #     detection_result = detector.detect(mp_image)

# # #     if detection_result.hand_landmarks:
# # #         landmarks = detection_result.hand_landmarks[0]
# # #         index = landmarks[8]
# # #         thumb = landmarks[4]

# # #         # 1. COORDINATE MAPPING (with Deadzone)
# # #         # Map a smaller inner rectangle of the webcam to the full screen
# # #         ix = int(math.hypot(index.x * w, 0)) # simplified x
# # #         iy = int(math.hypot(index.y * h, 0)) # simplified y
        
# # #         target_x = (index.x * w - frame_reduction) * screen_w / (w - 2 * frame_reduction)
# # #         target_y = (index.y * h - frame_reduction) * screen_h / (h - 2 * frame_reduction)

# # #         # 2. SMOOTHING (Interpolation)
# # #         curr_x = prev_x + (target_x - prev_x) / SMOOTHING
# # #         curr_y = prev_y + (target_y - prev_y) / SMOOTHING
        
# # #         pyautogui.moveTo(curr_x, curr_y)
# # #         prev_x, prev_y = curr_x, curr_y

# # #         # 3. NON-BLOCKING CLICK LOGIC
# # #         distance = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2)
# # #         current_time = time.time()
        
# # #         if distance < 0.05: # Threshold
# # #             cv2.circle(frame, (int(index.x*w), int(index.y*h)), 15, (0, 0, 255), -1)
# # #             # Only click if 0.3s has passed since last click (non-blocking)
# # #             if current_time - last_click_time > 0.3:
# # #                 pyautogui.click()
# # #                 last_click_time = current_time
# # #         else:
# # #             cv2.circle(frame, (int(index.x*w), int(index.y*h)), 10, (0, 255, 0), -1)

# # #     cv2.imshow('PBL Hand Control', frame)
# # #     if cv2.waitKey(1) & 0xFF == ord('q'):
# # #         break

# # # cap.release()
# # # cv2.destroyAllWindows()









# # # import cv2
# # # import mediapipe as mp
# # # from mediapipe.tasks import python
# # # from mediapipe.tasks.python import vision
# # # import pyautogui
# # # import math

# # # # 1. Setup
# # # base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
# # # options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
# # # detector = vision.HandLandmarker.create_from_options(options)

# # # cap = cv2.VideoCapture(0)
# # # screen_w, screen_h = pyautogui.size()

# # # # Smoothing variables
# # # smooth_x, smooth_y = 0, 0
# # # closeness_threshold = 0.05  # Adjust this for click sensitivity

# # # while cap.isOpened():
# # #     success, frame = cap.read()
# # #     if not success: break

# # #     frame = cv2.flip(frame, 1)
# # #     h, w, _ = frame.shape
# # #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# # #     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

# # #     detection_result = detector.detect(mp_image)

# # #     if detection_result.hand_landmarks:
# # #         for landmarks in detection_result.hand_landmarks:
# # #             # Get landmarks for Index (8) and Thumb (4)
# # #             index = landmarks[8]
# # #             thumb = landmarks[4]

# # #             # 1. MOUSE MOVEMENT (with basic smoothing)
# # #             target_x = index.x * screen_w
# # #             target_y = index.y * screen_h
            
# # #             # Smoothing formula: current = current + (target - current) * factor
# # #             smooth_x = smooth_x + (target_x - smooth_x) * 0.5
# # #             smooth_y = smooth_y + (target_y - smooth_y) * 0.5
            
# # #             pyautogui.moveTo(smooth_x, smooth_y, _pause=False)

# # #             # 2. CLICK LOGIC (Distance between thumb and index)
# # #             distance = math.sqrt((index.x - thumb.x)**2 + (index.y - thumb.y)**2)
            
# # #             if distance < closeness_threshold:
# # #                 cv2.circle(frame, (int(index.x*w), int(index.y*h)), 15, (0, 0, 255), -1) # Red for click
# # #                 pyautogui.click()
# # #                 pyautogui.sleep(0.2) # Prevent accidental double-clicks
# # #             else:
# # #                 cv2.circle(frame, (int(index.x*w), int(index.y*h)), 10, (0, 255, 0), -1) # Green for hover

# # #     cv2.imshow('PBL Hand Control', frame)
# # #     if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('PBL Hand Control', cv2.WND_PROP_VISIBLE) < 1:
# # #         break

# # # cap.release()
# # # cv2.destroyAllWindows()
