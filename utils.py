import numpy as np
import cv2
from collections import deque


# Distance Utility
def get_distance_obj(p1, p2):
    """Euclidean distance between two MediaPipe landmarks."""
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# EAR Smoother

class EARSmoother:
    def __init__(self, window_size=5):
        self.buffer = deque(maxlen=window_size)

    def update(self, ear):
        self.buffer.append(ear)
        return np.mean(self.buffer)

# UI Overlay

def draw_ui(frame, gaze_dir, blink_state, hold_time, mode):

    cv2.putText(frame, f"Gaze: {gaze_dir}", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.putText(frame, f"Blink: {blink_state}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.putText(frame, f"Mode: {mode}", (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2)

    if hold_time > 0:
        cv2.putText(frame, f"Hold: {hold_time:.1f}s", (20, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)


def draw_gaze_indicator(frame, landmarks, eye_tracker, img_w, img_h):

    # Get landmarks
    left = landmarks[eye_tracker.LEFT_EYE_LEFT_CORNER]
    right = landmarks[eye_tracker.LEFT_EYE_RIGHT_CORNER]
    iris = landmarks[eye_tracker.LEFT_IRIS_CENTER]

    # Convert to pixel coordinates
    left_px = (int(left.x * img_w), int(left.y * img_h))
    right_px = (int(right.x * img_w), int(right.y * img_h))
    iris_px = (int(iris.x * img_w), int(iris.y * img_h))

    # Eye center (midpoint)
    eye_center_px = (
        int((left_px[0] + right_px[0]) / 2),
        int((left_px[1] + right_px[1]) / 2)
    )

    # Drawing eye center (green colour)
    cv2.circle(frame, eye_center_px, 4, (0, 255, 0), -1)

    # Drawing iris center (red colour)
    cv2.circle(frame, iris_px, 4, (0, 0, 255), -1)

    # Draw gaze direction vector (yellow colour)
    cv2.line(frame, eye_center_px, iris_px, (0, 255, 255), 1)
    mid_y = (left_px[1] + right_px[1]) // 2
    cv2.line(frame, (0, mid_y), (img_w, mid_y), (0, 255, 255), 1)

# EAR Calculation

def get_ear(eye_points_indices, landmarks):
    """Calculates EAR using landmark object attributes."""
    p = [landmarks[i] for i in eye_points_indices]
    
    # Vertical distances
    v1 = get_distance_obj(p[1], p[5])
    v2 = get_distance_obj(p[2], p[4])
    # Horizontal distance
    h = get_distance_obj(p[0], p[3])
    
    return (v1 + v2) / (2.0 * h)