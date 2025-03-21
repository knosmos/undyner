import cv2
import numpy as np
import time
import mss

# writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20, (640, 480))
# mp4
writer = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 20, (640, 480))

# Create some random colors
color = np.random.randint(0, 255, (100, 3))
prvs = None
with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 50, "left": 0, "width": 640, "height": 480}

    while "Screen capturing":
        last_time = time.time()
        img = np.array(sct.grab(monitor))
        img = img[:, :, 0:3]
        writer.write(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imshow("screenshot", img)

        print(f"fps: {1 / (time.time() - last_time)}")

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
