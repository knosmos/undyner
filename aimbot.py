import cv2
import numpy as np
import mss
import keyboard
import time

BOX_SIZE = (10, 400)
TOPLEFT = (280, 40)
BOX = (TOPLEFT[0], TOPLEFT[1], TOPLEFT[0] + BOX_SIZE[0], TOPLEFT[1] + BOX_SIZE[1])

WHITE_MIN = (240, 240, 240)
WHITE_MAX = (255, 255, 255)

enabled = False
key = None

def toggle():
    global enabled
    enabled = not enabled
    print("!! ENABLED !!" if enabled else "!! DISABLED !!")
    if key:
        keyboard.release(key)


keyboard.add_hotkey("w", toggle)

detections = []
start = time.time_ns() // 1000000

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
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 1 and 5 < cv2.contourArea(contours[0]) < 100:
            x, y, w, h = cv2.boundingRect(contours[0])
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # cv2.circle(frame, (x + w // 2, y + h // 2), 5, (255, 0, 0), -1)
            detections.append((x + w // 2, time.time_ns() // 1000000 - start))
        
        if len(detections) > 4:
            detections.pop(0)
        
    
        while detections and detections[0][0] == 220 \
            or (
                len(detections) > 1 and (
                    detections[0][0] == detections[1][0] \
                    or time.time_ns() // 1000000 - start - detections[0][1] > 1000
                )
            ):
            detections.pop(0)
        
        if len(detections) >= 4:
            #print(detections)
            # predict time of center
            # speeds = [
            #     (detections[i][0] - detections[i-1][0]) /
            #     (detections[i][1] - detections[i-1][1])
            #     for i in range(1, len(detections))
            # ]
            # if speeds[-1] != 0:
            #     avg_speed = sum(speeds) / len(speeds)
            avg_speed = (detections[-1][0] - detections[0][0]) / (detections[-1][1] - detections[0][1])
            if avg_speed != 0:
                #print(avg_speed)
                dist = BOX_SIZE[1] / 2 - detections[-1][0]
                time_to_center = dist / avg_speed
                time_to_center -= time.time_ns() // 1000000 - start - detections[-1][1]
                #print("time to center :", time_to_center)
                keyboard.release("z")
                if time_to_center < 50:
                    print("firing!")
                    if enabled:
                        # keyboard.press("z")
                        time.sleep(0.01)

        cv2.imshow("output", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
