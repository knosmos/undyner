import cv2
import numpy as np
import mss
import keyboard

video = cv2.VideoCapture("white_attack.mp4")

BOX_SIZE = 150
TOPLEFT = (210, 240)
BOX = (TOPLEFT[0], TOPLEFT[1], TOPLEFT[0] + BOX_SIZE, TOPLEFT[1] + BOX_SIZE)

RED_MIN = (0, 0, 100)
RED_MAX = (80, 80, 255)

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
        mask = cv2.inRange(frame, RED_MIN, RED_MAX)
        M = cv2.moments(mask)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)

            # hough lines
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            cv2.imshow("edges", edges)
            lines = cv2.HoughLines(edges, 1, np.pi/180, 30)
            trajectory_map = np.zeros_like(gray)
            if lines is not None:
                for rho, theta in lines[:, 0]:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * -b)
                    y1 = int(y0 + 1000 * a)
                    x2 = int(x0 - 1000 * -b)
                    y2 = int(y0 - 1000 * a)
                    cv2.line(trajectory_map, (x1, y1), (x2, y2), 255, 2)

            cv2.imshow("trajectory", trajectory_map)

            # test for intersection in frame
            fov = 20
            playerbox = (cX - fov, cY - fov, cX + fov, cY + fov)
            sample = trajectory_map[playerbox[0]:playerbox[2], playerbox[1]:playerbox[3]]

            if cv2.countNonZero(sample) == 0:
                print("no intersection")
            else:
                areas = [
                    (sample[0:fov, :], "up"),
                    (sample[:, 0:fov], "left"),
                    (sample[:, fov:], "right"),
                    (sample[fov:, :], "down")
                ]
                best = None
                for area, direction in areas:
                    intersections = cv2.countNonZero(area)
                    if best is None or intersections < best[0]:
                        best = (intersections, direction)
                print(best)

                if enabled:
                    if key:
                        keyboard.release(key)
                    keyboard.press(best[1])
                    key = best[1]
        
        cv2.imshow("output", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break