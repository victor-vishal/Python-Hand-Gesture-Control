# core/config.py

class Config:
    # --- MODEL PATH ---
    # Make sure 'hand_landmarker.task' is in the root folder of your project
    MODEL_PATH = 'hand_landmarker.task'

    # --- MOUSE SETTINGS ---
    SENSITIVITY = 3.5      
    SMOOTHING = 5         
    CLICK_THRESHOLD = 0.07 
    RIGHT_CLICK_COOLDOWN = 0.5 

    # --- HUD VISUALS ---
    # Custom skeleton connections to avoid MediaPipe version errors
    HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),         # Thumb
        (5, 6), (6, 7), (7, 8),                 # Index
        (9, 10), (10, 11), (11, 12),            # Middle
        (13, 14), (14, 15), (15, 16),           # Ring
        (17, 18), (18, 19), (19, 20),           # Pinky
        (0, 5), (5, 9), (9, 13), (13, 17), (0, 17) # Palm Base
    ]