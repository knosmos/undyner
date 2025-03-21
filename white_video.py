import cv2
import numpy as np

video = cv2.VideoCapture("white_attack.mp4")

BOX_SIZE = 150
TOPLEFT = (210, 240)
BOX = (TOPLEFT[0], TOPLEFT[1], TOPLEFT[0] + BOX_SIZE, TOPLEFT[1] + BOX_SIZE)

RED_MIN = (0, 0, 100)
RED_MAX = (80, 80, 255)

fov = 50

while True:
    ret, frame = video.read()
    if not ret:
        break

    # crop
    frame = frame[BOX[0]:BOX[2], BOX[1]:BOX[3]]
    frame = cv2.copyMakeBorder(frame, fov, fov, fov, fov, cv2.BORDER_CONSTANT, value=0)

    # detect player
    mask = cv2.inRange(frame, RED_MIN, RED_MAX)
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
    else:
        continue

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
    playerbox = (cX - fov, cY - fov, cX + fov, cY + fov)
    sample = trajectory_map[playerbox[1]:playerbox[3], playerbox[0]:playerbox[2]]
    print(sample.shape)

    sample = cv2.dilate(sample, np.ones((10, 10), np.uint8))
    cv2.imshow("sample", sample)

    if cv2.countNonZero(sample) == 0:
        print("no intersection")
    else:
        areas = [
            (sample[0:fov, :], "top"),
            (sample[:, 0:fov], "left"),
            (sample[:, fov:], "right"),
            (sample[fov:, :], "bottom")
        ]
        best = None
        for area, direction in areas:
            intersections = cv2.countNonZero(area)
            if best is None or intersections < best[0]:
                best = (intersections, direction)
        print(best)
    
    cv2.imshow("output", frame)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break