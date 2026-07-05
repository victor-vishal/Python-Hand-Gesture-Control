# main.py
import cv2
import pyautogui
from core.hand_tracker import HandTracker
from core.mouse_engine import MouseEngine
from core.config import Config

def main():
    print("Starting Python Hand Gesture Control...")
    print("Press 'q' to quit.")
    print("Press 'm' to toggle Picture-in-Picture mode.")
    
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    mouse = MouseEngine()
    
    pip_mode = False
    window_name = 'Hand Gesture Control HUD'
    
    # We use WINDOW_NORMAL so we can resize it via code
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        # 1. Get AI Landmarks
        landmarks = tracker.get_landmarks(frame)
        
        if landmarks:
            # 2. Draw Custom Skeleton
            for connection in Config.HAND_CONNECTIONS:
                start_idx, end_idx = connection
                start_pos = (int(landmarks[start_idx].x * w), int(landmarks[start_idx].y * h))
                end_pos = (int(landmarks[end_idx].x * w), int(landmarks[end_idx].y * h))
                cv2.line(frame, start_pos, end_pos, (255, 0, 255), 2)
                
            for lm in landmarks:
                pos = (int(lm.x * w), int(lm.y * h))
                cv2.circle(frame, pos, 4, (0, 255, 255), -1)

            # 3. Process Gestures & Mouse
            status_text, status_color = mouse.process_frame(landmarks, w, h)
            cv2.putText(frame, f'Status: {status_text}', (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        else:
            cv2.putText(frame, 'Searching for Hand...', (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 4. Draw Active Zone (Hide it if we are in PiP mode)
        if not pip_mode:
            cv2.rectangle(frame, (int(w*0.2), int(h*0.2)), (int(w*0.8), int(h*0.8)), (255, 255, 255), 1)
            
        cv2.imshow(window_name, frame)
        
        # 5. Keyboard Controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'):
            pip_mode = not pip_mode
            if pip_mode:
                # Shrink window and force it Always On Top
                cv2.resizeWindow(window_name, 350, 250)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
                print("PiP Mode ON")
            else:
                # Restore to normal size and remove Always On Top
                cv2.resizeWindow(window_name, 640, 480)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 0)
                print("PiP Mode OFF")

    # Fail-safe cleanup
    if mouse.is_dragging:
        pyautogui.mouseUp(button='left')
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()