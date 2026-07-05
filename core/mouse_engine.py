# core/mouse_engine.py
import pyautogui
import math
import time
import numpy as np
from core.config import Config

class MouseEngine:
    def __init__(self):
        pyautogui.PAUSE = 0
        self.screen_w, self.screen_h = pyautogui.size()
        
        # Start mouse in the center
        self.prev_x, self.prev_y = self.screen_w // 2, self.screen_h // 2
        
        # State trackers
        self.is_dragging = False
        self.last_right_click_time = 0
        self.last_swipe_time = 0
        self.prev_palm_x = None

    def get_distance(self, p1, p2):
        """Calculates distance between two landmarks."""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def get_fingers_up(self, landmarks):
        """Checks which fingers are currently extended."""
        # We compare the Tip (8, 12, 16, 20) to the pip joint below it (6, 10, 14, 18)
        # If the tip is higher (lower y value), the finger is open.
        fingers = []
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        for tip, pip in zip(tips, pips):
            fingers.append(landmarks[tip].y < landmarks[pip].y)
        return fingers # Returns [Index, Middle, Ring, Pinky]

    def process_frame(self, landmarks, w, h):
        """Main engine that translates landmarks into mouse actions."""
        thumb = landmarks[4]
        index = landmarks[8]
        palm = landmarks[9]  # Steer
        middle = landmarks[12] 
        pinky = landmarks[20]

        # 1. Check Distances & Finger States
        dist_left_click = self.get_distance(index, thumb)
        dist_right_click = self.get_distance(pinky, thumb)
        dist_media = self.get_distance(middle, thumb) # <--- ADD THIS
        
        fingers_up = self.get_fingers_up(landmarks)
        is_peace_sign = fingers_up[0] and fingers_up[1] and not fingers_up[2] and not fingers_up[3]
        is_flat_hand = all(fingers_up) # All 4 fingers are up

        current_time = time.time()
        status_text = "Hovering"
        status_color = (0, 255, 0) # Green

        # 2. Movement Math (Steering with the Palm)
        offset_x = (palm.x - 0.5) * Config.SENSITIVITY
        offset_y = (palm.y - 0.5) * Config.SENSITIVITY
        target_x = (0.5 + offset_x) * self.screen_w
        target_y = (0.5 + offset_y) * self.screen_h

        curr_x = self.prev_x + (target_x - self.prev_x) / Config.SMOOTHING
        curr_y = self.prev_y + (target_y - self.prev_y) / Config.SMOOTHING
        
        final_x = np.clip(curr_x, 2, self.screen_w - 2)
        final_y = np.clip(curr_y, 2, self.screen_h - 2)

        # --- UNIVERSAL SAFETY RELEASE ---
        # If we were dragging, but the fingers are no longer pinched, drop the mouse immediately.
        # This prevents the drag from getting stuck if you accidentally switch gestures.
        if self.is_dragging and dist_left_click >= Config.CLICK_THRESHOLD:
            pyautogui.mouseUp(button='left')
            self.is_dragging = False

        # --- GESTURE ROUTER ---
        
        # Reset the swipe tracker safely outside the main chain
        if not is_flat_hand:
            self.prev_palm_x = None

        # Gesture 1: Alt + Tab (Swipe with Flat Hand)
        if is_flat_hand:
            status_text = "Ready to Swipe"
            status_color = (255, 255, 0) # Cyan
            if self.prev_palm_x is not None:
                movement_x = palm.x - self.prev_palm_x
                if abs(movement_x) > 0.05 and (current_time - self.last_swipe_time > 1.0):
                    if movement_x > 0: 
                        pyautogui.hotkey('alt', 'tab')
                        status_text = "Swiped Right!"
                    else: 
                        pyautogui.hotkey('alt', 'shift', 'tab')
                        status_text = "Swiped Left!"
                    self.last_swipe_time = current_time
            self.prev_palm_x = palm.x

            # --- ADD THIS LINE SO IT DOESN'T TELEPORT LATER ---
            pyautogui.moveTo(final_x, final_y) 
            self.prev_x, self.prev_y = final_x, final_y

        # Gesture 2: Vertical Scrolling (Peace Sign)
        elif is_peace_sign:
            status_text = "Scrolling"
            status_color = (255, 165, 0) # Orange
            # Calculate how much the hand moved up or down since last frame
            delta_y = target_y - self.prev_y
            if abs(delta_y) > 5: 
                scroll_amount = int(-delta_y * 0.5) 
                pyautogui.scroll(scroll_amount)

            # --- ADD THIS LINE SO IT DOESN'T TELEPORT LATER ---
            pyautogui.moveTo(final_x, final_y) 
            self.prev_x, self.prev_y = final_x, final_y

        # Gesture: Volume Control (Thumb + Middle)
        elif dist_media < Config.CLICK_THRESHOLD:
            status_text = "Volume Control"
            status_color = (255, 0, 255) # Magenta
            
            # Calculate vertical movement
            delta_y = target_y - self.prev_y
            
            # Use a deadzone so it doesn't change volume if your hand is still
            if delta_y < -3: 
                pyautogui.press('volumeup')
            elif delta_y > 3:
                pyautogui.press('volumedown')
                
            pyautogui.moveTo(final_x, final_y) 
            self.prev_x, self.prev_y = final_x, final_y

        # Gesture 3: Right Click (Thumb + Pinky)
        elif dist_right_click < Config.CLICK_THRESHOLD:
            status_text = "Right Click"
            status_color = (255, 0, 0) # Blue
            if current_time - self.last_right_click_time > Config.RIGHT_CLICK_COOLDOWN:
                pyautogui.click(button='right')
                self.last_right_click_time = current_time
            pyautogui.moveTo(final_x, final_y)
            self.prev_x, self.prev_y = final_x, final_y

        # Gesture 4: Left Click / Drag (Thumb + Index)
        elif dist_left_click < Config.CLICK_THRESHOLD:
            status_text = "Dragging / Left Click"
            status_color = (0, 0, 255) # Red
            if not self.is_dragging:
                pyautogui.mouseDown(button='left')
                self.is_dragging = True
            pyautogui.moveTo(final_x, final_y)
            self.prev_x, self.prev_y = final_x, final_y

        # Gesture 5: Hover (Default state)
        else:
            if self.is_dragging:
                pyautogui.mouseUp(button='left')
                self.is_dragging = False
            pyautogui.moveTo(final_x, final_y)
            self.prev_x, self.prev_y = final_x, final_y

        return status_text, status_color