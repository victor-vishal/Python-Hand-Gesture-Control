import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui

# 1. Setup the Task (This is the new way)
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    # Convert BGR to RGB and create MediaPipe Image object
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detect landmarks
    detection_result = detector.detect(mp_image)

    # If hands are found, draw a simple circle on the index finger
    if detection_result.hand_landmarks:
        for landmarks in detection_result.hand_landmarks:
            # Landmark 8 is the index finger tip
            index_finger = landmarks[8]
            h, w, _ = frame.shape
            x, y = int(index_finger.x * w), int(index_finger.y * h)
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

    cv2.imshow('PBL Hand Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



# import cv2
# import mediapipe as mp
# # We bypass mp.solutions and go straight to the source
# from mediapipe.python.solutions import hands as mp_hands
# from mediapipe.python.solutions import drawing_utils as mp_draw
# import pyautogui

# # Initialize using the new direct references
# hands = mp_hands.Hands(
#     static_image_mode=False, 
#     max_num_hands=1, 
#     min_detection_confidence=0.7,
#     min_tracking_confidence=0.5
# )

# cap = cv2.VideoCapture(0)

# while True:
#     success, img = cap.read()
#     if not success: break
    
#     img = cv2.flip(img, 1)
#     # MediaPipe needs RGB, OpenCV gives BGR
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
#             mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            
#             # Index Finger Tip (Landmark 8)
#             index_tip = handLms.landmark[8]
#             h, w, _ = img.shape
#             cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            
#             # Visual feedback
#             cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

#     cv2.imshow("PBL Hand Tracker", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()




# # import mediapipe
# # print(f"DEBUG: MediaPipe is being loaded from: {mediapipe.__file__}")
# # import cv2
# # import mediapipe as mp
# # import pyautogui

# # # Initialize MediaPipe
# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
# # mp_draw = mp.solutions.drawing_utils

# # # Screen settings
# # screen_w, screen_h = pyautogui.size()
# # cap = cv2.VideoCapture(0)

# # while True:
# #     success, img = cap.read()
# #     if not success: break
    
# #     img = cv2.flip(img, 1)
# #     h, w, c = img.shape
# #     results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# #     if results.multi_hand_landmarks:
# #         for handLms in results.multi_hand_landmarks:
# #             mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            
# #             # Landmark 8 is the Index Finger Tip
# #             index_tip = handLms.landmark[8]
            
# #             # Map coordinates to screen size
# #             # We multiply by 1.5 to make it easier to reach corners without stretching
# #             mx = int(index_tip.x * screen_w)
# #             my = int(index_tip.y * screen_h)
            
# #             # Move the mouse cursor
# #             pyautogui.moveTo(mx, my, _pause=False)

# #     cv2.imshow("Hand Control", img)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()




# # # import cv2
# # # import mediapipe as mp
# # # import pyautogui

# # # # Initialize MediaPipe Hand tracking
# # # mp_hands = mp.solutions.hands
# # # hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
# # # mp_draw = mp.solutions.drawing_utils

# # # cap = cv2.VideoCapture(0)

# # # # This will make the text bright because the library is now "active"
# # # screenWidth, screenHeight = pyautogui.size() 
# # # print(f"Screen size: {screenWidth}x{screenHeight}")

# # # while True:
# # #     success, img = cap.read()
# # #     img = cv2.flip(img, 1) # Flip for mirror effect
# # #     h, w, c = img.shape
# # #     results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# # #     if results.multi_hand_landmarks:
# # #         for handLms in results.multi_hand_landmarks:
# # #             # Draw the landmarks on the screen
# # #             mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            
# # #             # Index finger tip is landmark #8
# # #             index_finger = handLms.landmark[8]
# # #             cx, cy = int(index_finger.x * w), int(index_finger.y * h)
            
# # #             # Draw a circle on the index tip
# # #             cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

# # #     cv2.imshow("Hand Tracker", img)
# # #     if cv2.waitKey(1) & 0xFF == ord('q'):
# # #         break

# # # cap.release()
# # # cv2.destroyAllWindows()