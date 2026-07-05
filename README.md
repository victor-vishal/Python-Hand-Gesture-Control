# 🖐️ Python Hand Gesture Control (AI Virtual Mouse)

A futuristic, highly responsive virtual mouse powered by AI. This project uses your webcam to track your hand in real-time, allowing you to control your computer's cursor, click, scroll, manage windows, and adjust media volume using natural hand gestures.

Built with Python, OpenCV, MediaPipe (Tasks API for high performance), and PyAutoGUI.

## ✨ Features

* **Zero-Lag Dynamic Smoothing:** Automatically adjusts cursor weight. Fast and snappy when moving, but slow and ultra-precise when you pinch to click.
* **Cyberpunk HUD:** A custom-drawn, lightweight skeleton overlay tracking 21 hand landmarks in real-time.
* **Picture-in-Picture (PiP) Mode:** Shrink the webcam feed into a borderless, "Always-on-Top" mini-window so you can work seamlessly.
* **Anti-Drift Steering:** Steers the cursor from the center of the palm rather than the fingertips, completely eliminating "pointer drift" when clicking.

## 🕹️ Gesture Dictionary

| Gesture | Physical Action | On-Screen Result |
| :--- | :--- | :--- |
| **Hover / Move** | Relaxed hand (Fingers open or closed) | Moves the cursor. |
| **Left Click / Drag** | Pinch **Thumb + Index Finger** | Left clicks. Hold and move to drag windows/highlight. |
| **Right Click** | Pinch **Thumb + Pinky Finger** | Triggers a right-click menu. |
| **Scroll Up/Down** | **Peace Sign** (Index + Middle up) | Locks cursor; move hand vertically to scroll pages. |
| **Volume Control** | Pinch **Thumb + Middle Finger** | Move hand up/down to adjust system volume. |
| **Switch Apps** | **Flat Hand** (All 5 fingers up) | Swipe Right = `Alt+Tab`. Swipe Left = `Alt+Shift+Tab`. |

## ⚙️ Keyboard Controls (When window is focused)

* Press `m` — Toggle Picture-in-Picture (PiP) mode.
* Press `q` — Safely quit the application (includes an auto-drop failsafe for dragging).

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/python-hand-gesture-control.git](https://github.com/YOUR_USERNAME/python-hand-gesture-control.git)
   cd python-hand-gesture-control
  ```

   
   
2. **Install the dependencies:**

   It is recommended to use a virtual environment (`venv`).
   
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the MediaPipe Model:**

   This project uses the optimized MediaPipe Tasks API. You need to download the `hand_landmarker.task` file.

   Download it directly from Google here: [Hand Landmarker Task](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker)

   Place the `hand_landmarker.task` file directly in the root folder of this project.

4. **Run the engine:**

   ```bash
   python main.py
   ```

## 📂 Project Architecture

This project is built with a clean, object-oriented structure to make it easy to read and expand:

```plaintext
python-hand-gesture-control/
│
├── core/
│   ├── __init__.py
│   ├── config.py         # Master settings (Sensitivity, Smoothing, Thresholds)
│   ├── hand_tracker.py   # Handles MediaPipe AI and webcam processing
│   └── mouse_engine.py   # Handles PyAutoGUI math, gesture routing, and execution
│
├── hand_landmarker.task  # (You must download this file)
├── requirements.txt      # Project dependencies
├── README.md             
└── main.py               # The main conductor and GUI loop
```

## 🛠️ Configuration 

You can easily tweak the feel of the mouse by editing `core/config.py`.

* **SENSITIVITY**: Increase this if you want the mouse to move further with less hand movement.
* **CLICK_THRESHOLD**: Tweak this if you want the pinching gestures to trigger earlier or later.
