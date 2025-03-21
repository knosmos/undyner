import cv2
import numpy as np
import mss
import keyboard
import time

video = cv2.VideoCapture("white_attack.mp4")

BOX_SIZE = 80
TOPLEFT = (280, 280)
BOX = (TOPLEFT[0], TOPLEFT[1], TOPLEFT[0] + BOX_SIZE, TOPLEFT[1] + BOX_SIZE)

WHITE_MIN = (240, 240, 240)
WHITE_MAX = (255, 255, 255)

enabled = False
key = None

def toggle():
    global enabled
    enabled = not enabled
    print("enabled" if enabled else "disabled")
    if key:
        keyboard.release(key)


keyboard.add_hotkey("w", toggle)

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 50, "left": 0, "width": 640, "height": 480}

    while True:
        frame = np.array(sct.grab(monitor))
        frame = frame[:, :, 0:3]
        cv2.imshow("screenshot", frame)

        # crop
        frame = frame[BOX[0]:BOX[2], BOX[1]:BOX[3]]

        # detect player
        mask = cv2.inRange(frame, WHITE_MIN, WHITE_MAX)

        M = cv2.moments(mask)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if 30 < cX < 50:
                keyboard.release("enter")
                if enabled:
                    keyboard.press("enter")
                print("firing!")
        
        cv2.imshow("output", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break