# Hand Gesture Mouse Control

A Python project that lets you control your computer's mouse using hand gestures tracked live through a webcam — no extra hardware required. Move your cursor by pointing your index finger, and left/right-click using a pinch gesture, with movement smoothed using a custom-built PID controller.

## How it works

1. **Webcam capture** — OpenCV reads live frames from the webcam.
2. **Hand detection** — MediaPipe (via the `cvzone` wrapper) detects the hand in each frame and returns 21 landmark points (fingertips, knuckles, wrist).
3. **Coordinate mapping** — the index fingertip's position is extracted and rescaled from webcam coordinates into full screen coordinates using linear interpolation, so a small, comfortable hand movement covers the whole screen.
4. **Gesture recognition** — finger positions are checked each frame to switch between "moving mode" (thumb + index up, middle down) and "clicking mode" (thumb + index + middle up, with a pinch between index and middle triggering a click).
5. **Click debouncing** — background threads add a short cooldown after each click, preventing a single pinch from firing dozens of rapid clicks.
6. **PID-smoothed movement** — instead of jumping straight to the target position each frame, a custom Proportional-Derivative controller gradually moves the cursor toward the target, removing jitter from small hand tremors while staying responsive.

## Tech stack

- **Python**
- **OpenCV** (`opencv-contrib-python`) — webcam capture and drawing
- **MediaPipe** (via `cvzone`) — hand landmark detection
- **NumPy** — coordinate interpolation
- **mouse** — moving the cursor and triggering clicks
- **threading** — non-blocking click cooldown timers

## Setup

1. Install the required packages:
2. Run the script:
3. A window will open showing your webcam feed with hand landmarks drawn on it. Hold your thumb and index finger up (middle down) to move the cursor; bring your index and middle fingers together while all three are up to click.

## Controls

| Gesture | Action |
|---|---|
| Thumb + index up, middle down | Move cursor |
| Thumb + index + middle up, pinch index/middle together, pinky down | Left click |
| Thumb + index + middle up, pinch index/middle together, pinky up | Right click |

## Notes

- Tracking works best in reasonably well-lit conditions.
- PID gains (`Kp`, `Kd`) can be tuned in the script to adjust the trade-off between responsiveness and smoothness.