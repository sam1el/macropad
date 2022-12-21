# SPDX-FileCopyrightText: 2022 Tali Herzka
#
# SPDX-License-Identifier: MIT

"""Keypad and rotary encoder example for Adafruit MacroPad"""
import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_macropad import MacroPad
import usb_hid

MACRO_FOLDER = '/macros'

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
        group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()



macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False
pixels = macropad.pixels

kbd = Keyboard(usb_hid.devices)

right = Keycode.RIGHT_ARROW
left = Keycode.LEFT_ARROW
ctrl = Keycode.LEFT_CONTROL
cmd = Keycode.COMMAND
shift = Keycode.LEFT_SHIFT
opt = Keycode.OPTION
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (204, 245, 2)
WHITE = (255, 255, 255)

# maps the numeric macropad key number to a tuple containing an list of key(s) to send
# and the color to set the key to on the macropad
KEY_MAP = {
    0: ([], WHITE),
    1: ([], WHITE),
    2: ([], WHITE),
    3: ([], WHITE),
    4: ([], WHITE),
    5: ([], WHITE),
    6: ([], WHITE),
    7: ([], WHITE),
    8: ([], WHITE),
    # toggle zoom audio
    9: ([cmd, shift, Keycode.A], RED),

    # toggle zoom video
    10: ([cmd, shift, Keycode.V], RED),

    # toggle zoom floating meeting controls
    11: ([ctrl, opt, cmd, Keycode.H], YELLOW)
}

# set initial key colors and brightness
pixels.brightness = 0.2
for k, v in KEY_MAP.items():
    pixels[k] = v[1]
    pixels.show()

# WARNING: this will only be your initial state when you start a meeting if your Zoom settings are set to
# "mute my mic when joining a meeting" and "stop my video when joining a meeting" and will only accurately
# reflect your state if you don't toggle these manually via the zoom UI
vol_state = False
video_state = False

## set initial display text
text = macropad.display_text(text_scale=2)
text[0].text = "MUTED"
text[1].text = "VIDEO OFF"

# set initial encoder position
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, -2),
                         anchor_point=(0.5, 0.0)))
macropad.display.show(group)

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            print("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()

# Toggle LED from green to red or vice-versa
# uncomment the audio lines to play a sound when toggling
# (you must add the audio files to an audio directory and name the files accordingly)

# ON_AUDIO = "audio/on-tone.mp3"
# OFF_AUDIO = "audio/off-tone.mp3"

def toggle_led_and_sound(key_num):
    if pixels[key_num] not in [RED, GREEN]:
        return
    if pixels[key_num] == GREEN:
        # macropad.play_file(OFF_AUDIO)
        pixels[key_num] = RED
    else:
        # macropad.play_file(ON_AUDIO)
        pixels[key_num] = GREEN

while True:
    position = macropad.encoder
    if position != last_position:
        app_index = position % len(apps)
        apps[app_index].switch()
        last_position = position

    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        if len(apps[app_index].macros) < 13:
            continue    # No 13th macro, just resume main loop
        key_number = 12 # else process below as 13th macro
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed
    # send keyboard events mapped to keypad

    sequence = apps[app_index].macros[key_number][2]
    if pressed:
        # 'sequence' is an arbitrary-length list, each item is one of:
        # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
        # Negative integer: (absolute value) key released
        # Float (e.g. 0.25): delay in seconds
        # String (e.g. "Foo"): corresponding keys pressed & released
        # List []: one or more Consumer Control codes (can also do float delay)
        # Dict {}: mouse buttons/motion (might extend in future)
        key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            key_num = key_event.key_number
            keys_to_send = KEY_MAP.get(key_num)[0]
            if keys_to_send:
                # toggle zoom video
                if key_num == 9:
                    video_state = not video_state
                    text[1].text = "VIDEO {}".format("ON" if video_state else "OFF")

                # toggle zoom audio
                if key_num == 10:
                    vol_state = not vol_state
                    text[0].text = "{}MUTED".format("NOT " if vol_state else "")

                toggle_led_and_sound(key_num)

                keys_to_press = KEY_MAP[key_num][0]
                if keys_to_press:
                    kbd.press(*keys_to_press)
                kbd.release_all()
    else:
        # Release any still-pressed keys, consumer codes, mouse buttons
        # Keys and mouse buttons are individually released this way (rather
        # than release_all()) because pad supports multi-key rollover, e.g.
        # could have a meta key or right-mouse held down by one macro and
        # press/release keys/buttons with others. Navigate popups, etc.
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.release(item)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.release(item['buttons'])
                elif 'tone' in item:
                    macropad.stop_tone()
        macropad.consumer_control.release()
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
