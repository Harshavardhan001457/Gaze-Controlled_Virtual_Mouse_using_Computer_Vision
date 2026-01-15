class EyeTracker:
    def __init__(self):
        # MediaPipe FaceMesh indices (LEFT eye)
        self.LEFT_EYE_LEFT_CORNER = 33
        self.LEFT_EYE_RIGHT_CORNER = 133
        self.LEFT_IRIS_CENTER = 468

        # Tunable thresholds (safe defaults)
        self.H_LEFT_THRESH = 0.43
        self.H_RIGHT_THRESH = 0.57

        self.V_UP_THRESH = 0.003
        self.V_DOWN_THRESH = 0.001

        self.CENTER_DEADZONE = 0.04

    def get_gaze_direction(self, landmarks):
        left = landmarks[self.LEFT_EYE_LEFT_CORNER]
        right = landmarks[self.LEFT_EYE_RIGHT_CORNER]
        iris = landmarks[self.LEFT_IRIS_CENTER]

        # Horizontal gaze

        eye_width = right.x - left.x
        if eye_width == 0:
            return "CENTER"

        horizontal_ratio = (iris.x - left.x) / eye_width

        if horizontal_ratio < self.H_LEFT_THRESH:
            return "LEFT"
        elif horizontal_ratio > self.H_RIGHT_THRESH:
            return "RIGHT"


        # Vertical gaze

        eye_mid_y = (left.y + right.y) / 2
        vertical_offset = iris.y - eye_mid_y

        if vertical_offset < -self.V_UP_THRESH:
            return "UP"
        elif vertical_offset > self.V_DOWN_THRESH:
            return "DOWN"

        return "CENTER"