import green
import white
import aimbot

import mss

attacks = [
    "green",
    "green",
    "green",
    "white",
]

for attack in attacks:
    while True:
        if attack == "green":
            ret = green.main()
        elif attack == "white":
            ret = white.main()
        elif attack == "aimbot":
            ret = aimbot.main()
        else:
            break
        