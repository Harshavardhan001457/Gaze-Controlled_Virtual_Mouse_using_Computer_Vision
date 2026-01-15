import pyautogui
import time

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

        self.move_speed = 20
        self.last_move_time = 0
        self.move_interval = 0.02  # limits jitter (50 FPS)

        self.hold_start_time = None
        self.hold_triggered = False

        self.click_cooldown = 0.6
        self.last_click_time = 0

        pyautogui.PAUSE = 0

    # Cursor Movement

    def move_by_direction(self, direction):
        now = time.time()

        if now - self.last_move_time < self.move_interval:
            return

        if direction == "LEFT":
            pyautogui.moveRel(-self.move_speed, 0)
        elif direction == "RIGHT":
            pyautogui.moveRel(self.move_speed, 0)
        elif direction == "UP":
            pyautogui.moveRel(0, -self.move_speed)
        elif direction == "DOWN":
            pyautogui.moveRel(0, self.move_speed)
        # CENTER → no movement

        self.last_move_time = now


    # Gaze Hold (CENTER)

    def handle_gaze_hold(self, direction):
        now = time.time()

        if direction == "CENTER":
            if self.hold_start_time is None:
                self.hold_start_time = now
                self.hold_triggered = False

            elif not self.hold_triggered and (now - self.hold_start_time >= 3.0):
                if now - self.last_click_time >= self.click_cooldown:
                    pyautogui.click()
                    print("Gaze Hold: SELECT")
                    self.last_click_time = now
                    self.hold_triggered = True
        else:
            self.hold_start_time = None
            self.hold_triggered = False


    # Blink Click Actions

    def perform_click(self, clicks=1, button='left'):

        if clicks == 1 and button == 'left':
            pyautogui.click()
        elif button == 'right':
            pyautogui.rightClick()