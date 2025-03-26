import green
# import white_small
# import white_med
# import white_large
import aimbot_timer
import under_attack

import cv2
import numpy as np
import mss
import keyboard

attacks = [
    "green",
    "green",
    "green",
    "white",
]

keyboard.wait("s")

enabled = True
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
    
    for attack in attacks:
        print("== Running aimbot ==")
        aimbot_timer.run()
        print(f"== Running attack: {attack} ==")
        while True:
            if enabled:
                frame = np.array(sct.grab(monitor))
                frame = frame[:, :, 0:3]
                cv2.imshow("screenshot", frame)
                if attack == "green":
                    green.run(frame)
                # elif attack == "white":
                #     white.run(frame)
            if under_attack.attack_over(frame):
                print("attack over!")
                break
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
