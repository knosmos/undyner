import cv2
import keyboard
import time
import numpy as np

BOX_SIZE = 200
BOX = (
    480 // 2 - BOX_SIZE // 2,
    640 // 2 - BOX_SIZE // 2,
    480 // 2 + BOX_SIZE // 2,
    640 // 2 + BOX_SIZE // 2,
)

BATTLE_BOX = (BOX[0] + 60, BOX[1] + 60, BOX[2] - 60, BOX[3] - 60)

RED_MIN = (0, 0, 100)
RED_MAX = (80, 80, 255)

YELLOW_MIN = (0, 100, 100)
YELLOW_MAX = (80, 255, 255)

BLUE_MIN = (100, 0, 0)
BLUE_MAX = (255, 200, 80)

key = None

def run(frame):
    global key
    # black out area inside battle box
    frame[BATTLE_BOX[0] : BATTLE_BOX[2], BATTLE_BOX[1] : BATTLE_BOX[3]] = 0

    # crop
    frame = frame[BOX[0] : BOX[2], BOX[1] : BOX[3]]

    # red detection
    mask = cv2.inRange(frame, RED_MIN, RED_MAX)
    mask += cv2.inRange(frame, YELLOW_MIN, YELLOW_MAX)
    mask += cv2.inRange(frame, BLUE_MIN, BLUE_MAX)
    frame = cv2.bitwise_and(frame, frame, mask=mask)

    # contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bx, by = float("inf"), float("inf")
    for contour in contours:
        if cv2.contourArea(contour) < 5:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x += w // 2
        y += h // 2

        dx = x - 100
        dy = y - 100
        if dx * dx + dy * dy < (bx - 100) * (bx - 100) + (by - 100) * (by - 100):
            bx, by = x, y

    if bx != float("inf") and by != float("inf"):
        if key:
            keyboard.release(key)
        if bx < 70:
            key = "left"
        elif bx > 130:
            key = "right"
        elif by < 70:
            key = "up"
        elif by > 130:
            key = "down"
        keyboard.press(key)
        time.sleep(0.01)

        cv2.imshow("output", frame)
