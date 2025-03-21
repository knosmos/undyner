import cv2

video = cv2.VideoCapture("output.mp4")

BOX_SIZE = 200
BOX = (480//2 - BOX_SIZE//2, 640//2 - BOX_SIZE//2, 480//2 + BOX_SIZE//2, 640//2 + BOX_SIZE//2)

BATTLE_BOX = (BOX[0] + 60, BOX[1] + 60, BOX[2] - 60, BOX[3] - 60)

RED_MIN = (0, 0, 100)
RED_MAX = (80, 80, 255)

while True:
    ret, frame = video.read()
    if not ret:
        break

    # black out area inside battle box
    frame[BATTLE_BOX[0]:BATTLE_BOX[2], BATTLE_BOX[1]:BATTLE_BOX[3]] = 0

    # crop
    frame = frame[BOX[0]:BOX[2], BOX[1]:BOX[3]]

    # red detection
    mask = cv2.inRange(frame, RED_MIN, RED_MAX)
    frame = cv2.bitwise_and(frame, frame, mask=mask)

    # center of mass of red
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
    
        if cX < 70:
            print("left")
        elif cX > 130:
            print("right")
        elif cY < 70:
            print("up")
        elif cY > 130:
            print("down")
    
    cv2.imshow("output", frame)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break