import keyboard
import time
while 1:
    for i in range(10):
        keyboard.press("left")
        time.sleep(0.1)
        keyboard.release("left")
    for i in range(10):
        keyboard.press("right")
        time.sleep(0.1)
        keyboard.release("right")