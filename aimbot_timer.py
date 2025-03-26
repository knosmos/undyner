#import pyautogui
import keyboard
import time

def run_2():
    pyautogui.press("enter", interval=0.2)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.9)
    pyautogui.press("enter")
    time.sleep(1)

def run():
    keyboard.press("z")
    time.sleep(0.5)
    keyboard.release("z")
    time.sleep(0.5)
    keyboard.press("z")
    time.sleep(0.5)
    keyboard.release("z")
    time.sleep(0.4)
    keyboard.press("z")
    time.sleep(0.5)
    keyboard.release("z")
    time.sleep(1)

if __name__ == "__main__":
    keyboard.wait("w")
    run()