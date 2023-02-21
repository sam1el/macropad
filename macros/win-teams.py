# MACROPAD Hotkeys: Zoom for Mac


from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values


ctrl = Keycode.LEFT_CONTROL
shift = Keycode.LEFT_SHIFT
space = Keycode.SPACEBAR
alt = Keycode.ALT
right = Keycode.RIGHT_ARROW
left = Keycode.LEFT_ARROW
cmd = Keycode.COMMAND
opt = Keycode.OPTION
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (204, 245, 2)
WHITE = (255, 255, 255)


app = {  # REQUIRED dict, must be named 'app'

    "name": "MSFT Teams for Win",  # Application name
    "macros": [  # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (YELLOW, "Mute", [ctrl, shift, "M"]),  # Mute/Unmute
        (YELLOW, "TempUM", [ctrl, space]),  # Temporarily Unmute
        (YELLOW, "Video", [ctrl, shift, "O"]),  # turn on video
        # 2nd row ----------
        (GREEN, "Hand", [ctrl, shift, "K"]),  # RAISE HAND
        (WHITE, "Accept", [ctrl, shift, "A"]),  # Accept share
        (WHITE, "Share", [ctrl, shift, "E"]),  # Screen Sharing
        # 3rd row ----------
        (WHITE, "Announce", [ctrl, shift, "L"]),  # announce raised hands
        (WHITE, "Admit", [ctrl, shift, "Y"]),
        # 4th row ----------
        # Encoder button ---
    ],
}
