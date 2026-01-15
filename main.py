import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from utils import EARSmoother, draw_ui, draw_gaze_indicator, get_ear
from eye_tracker import EyeTracker
from mouse_controller import MouseController

# MediaPipe Task Setup

base_options = python.BaseOptions(model_asset_path="face_landmarker.task")
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1,
    running_mode=vision.RunningMode.VIDEO
)
detector = vision.FaceLandmarker.create_from_options(options)


# System Components

eye_tracker = EyeTracker()
mouse = MouseController()
ear_smoother = EARSmoother(window_size=5)


# Blink Configuration

LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

EAR_BLINK_THRESH = 0.21
blink_count = 0
last_blink_time = 0

# Camera

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    timestamp_ms = int(time.time() * 1000)
    result = detector.detect_for_video(mp_image, timestamp_ms)

    mode = "IDLE"
    gaze_dir = "CENTER"
    hold_time = 0
    blink_state = "NONE"

    if result.face_landmarks:
        landmarks = result.face_landmarks[0]
        img_h, img_w, _ = frame.shape

        # Draw gaze visualization
        
        draw_gaze_indicator(frame, landmarks, eye_tracker, img_w, img_h)

        # Gaze Direction

        gaze_dir = eye_tracker.get_gaze_direction(landmarks)
        mouse.move_by_direction(gaze_dir)
        mouse.handle_gaze_hold(gaze_dir)

        if gaze_dir != "CENTER":
            mode = "MOVING"
        else:
            mode = "HOLDING"

        if mouse.hold_start_time:
            hold_time = time.time() - mouse.hold_start_time

        # Blink Detection

        avg_ear = get_ear(LEFT_EYE_IDX, landmarks) # Simplified to one eye for trigger

        if avg_ear < EAR_BLINK_THRESH:
            current_time = time.time()
            if current_time - last_blink_time < 0.5:
                blink_count += 1
            else:
                blink_count = 1
            last_blink_time = current_time

            if blink_count == 2:
                mouse.perform_click(clicks=1)
                print("Double Blink -> Left Click")
            elif blink_count == 3:
                mouse.perform_click(button='right')
                print("Triple Blink -> Right Click")
            time.sleep(0.1)

    draw_ui(frame, gaze_dir, blink_state, hold_time, mode)

    cv2.imshow("Gaze Controlled Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

detector.close()
cap.release()
cv2.destroyAllWindows()