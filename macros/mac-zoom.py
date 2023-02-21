# MACROPAD Hotkeys: Zoom for Mac

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values
from adafruit_macropad import MacroPad

right = Keycode.RIGHT_ARROW
left = Keycode.LEFT_ARROW
ctrl = Keycode.LEFT_CONTROL
cmd = Keycode.COMMAND
shift = Keycode.LEFT_SHIFT
space = Keycode.SPACEBAR
opt = Keycode.OPTION
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (204, 245, 2)
WHITE = (255, 255, 255)


app = {  # REQUIRED dict, must be named 'app'

    "name": "Zoom",  # Application name
    "macros": [  # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (RED, "Mute", [cmd, shift, "A"]),  # Mute/Unmute
        (WHITE, "Record", [shift, cmd, "R"]),  # Local Record
        (RED, "TempUM", [space]),  # Temporarily Unmute
        # 2nd row ----------
        (RED, "Video", [shift, cmd, "V"]),  # Start/Stop Video
        (WHITE, "AltCam", [shift, cmd, "N"]),  # Switch Camera
        (WHITE, "Share", [shift, cmd, "S"]),  # Screen Sharing
        # 3rd row ----------
        (WHITE, "FullSc", [shift, cmd, "F"]),  # Full Screen
        (WHITE, "Control", [ctrl, opt, cmd, "H"]),
        (WHITE, "Gallery", [shift, cmd, "W"]),  # View
        # 4th row ----------
        # Encoder button ---
        (WHITE, "", [cmd, "W"]),  # Close Current Window
    ],
}
