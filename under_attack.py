import cv2

BOUNDS = [32, 434, 140, 480]

def attack_over(frame):
    fight_button = frame[BOUNDS[1]:BOUNDS[3], BOUNDS[0]:BOUNDS[2]]
    mask = cv2.inRange(fight_button, (60, 250, 250), (80, 255, 255))
    cv2.imshow("fight_button", mask)
    if cv2.countNonZero(mask) > 0:
        return True
