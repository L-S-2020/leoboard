import time
import board
import digitalio
import pwmio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.macros import Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.extensions import Extension

# ---------------- Layer IDs ----------------
L_NORMAL   = 0
L_GAMING   = 1
L_PREMIERE = 2
L_FN       = 3

# ---------------- Buzzer (simple, reliable) ----------------
import time
import pwmio
from kmk.extensions import Extension

class _BuzzerPlayer:
    def __init__(self, pin, duty_on=2**15):
        self.pin = pin
        self.duty_on = duty_on
        self.pwm = None
        self.seq = None
        self.i = 0
        self.until = 0.0
        self.playing = False
        self._init_pwm()

    def _init_pwm(self):
        if self.pwm:
            try:
                self.pwm.deinit()
            except Exception:
                pass
        self.pwm = pwmio.PWMOut(self.pin, variable_frequency=True, duty_cycle=0)

    def stop(self):
        # hard stop
        try:
            self.pwm.duty_cycle = 0
        except Exception:
            pass
        self.playing = False
        self.seq = None
        self.i = 0

    def play(self, seq):
        self.seq = list(seq)
        self.i = 0
        self.playing = True
        self._start_step()

    def _start_step(self):
        if not self.seq or self.i >= len(self.seq):
            self.stop()
            return
        freq, dur_ms = self.seq[self.i]
        if freq and freq > 0:
            self.pwm.frequency = int(freq)
            self.pwm.duty_cycle = self.duty_on
        else:
            self.pwm.duty_cycle = 0
        self.until = time.monotonic() + dur_ms / 1000.0

    def tick(self):
        if not self.playing:
            return
        if time.monotonic() >= self.until:
            self.i += 1
            self._start_step()
    
    def after_matrix_scan(self, sandbox):
        return
    
    def before_hid_send(self, sandbox):
        return
        
    def after_hid_send(self, sandbox):
        return

def _beep(n, freq=2200, on_ms=55, off_ms=55):
    out = []
    for k in range(n):
        out.append((freq, on_ms))
        if k != n - 1:
            out.append((0, off_ms))
    return out

def _startup():
    return [(1600, 40), (0, 25), (2400, 60), (0, 20)]

class LayerLEDs(Extension):
    def __init__(self, led_r, led_g, led_b, active_low=True):
        self.led_r, self.led_g, self.led_b = led_r, led_g, led_b
        self.active_low = active_low
        self.last = None

    def during_bootup(self, keyboard):
        # must exist or extension gets removed [page:0]
        self._all_off()

    def _on(self, led):
        led.value = False if self.active_low else True

    def _off(self, led):
        led.value = True if self.active_low else False

    def _all_off(self):
        self._off(self.led_r)
        self._off(self.led_g)
        self._off(self.led_b)

    def _set(self, base):
        self._all_off()
        if base == 0:
            self._on(self.led_r)
        elif base == 1:
            self._on(self.led_g)
        elif base == 2:
            self._on(self.led_b)

    def before_matrix_scan(self, sandbox):
        # sandbox.active_layers is refreshed every loop [page:0]
        layers = sandbox.active_layers or [0]
        base_candidates = [l for l in layers if l in (0, 1, 2)]
        base = max(base_candidates) if base_candidates else 0
        if base != self.last:
            self.last = base
            self._set(base)
    
    def after_matrix_scan(self, sandbox):
        return
    
    def before_hid_send(self, sandbox):
        return
        
    def after_hid_send(self, sandbox):
        return

class BuzzerSounds(Extension):
    def __init__(self, buzzer_pin):
        self.player = _BuzzerPlayer(buzzer_pin)
        self.last_base = None
        self.did_startup = False

    def during_bootup(self, keyboard):
        # must exist or extension gets removed [page:0]
        self.player.stop()
        self.last_base = None
        self.did_startup = False

    def before_matrix_scan(self, sandbox):
        # Always tick audio here (runs each loop) [page:0]
        self.player.tick()

        # Start-up sound once (first loop after boot)
        if not self.did_startup:
            self.did_startup = True
            self.player.play(_startup())
            return

        # Layer-change sound (base layer only)
        layers = sandbox.active_layers or [0]
        base_candidates = [l for l in layers if l in (0, 1, 2)]
        base = max(base_candidates) if base_candidates else 0

        if base != self.last_base:
            self.last_base = base
            self.player.play(_beep(base + 1))
    
    def after_matrix_scan(self, sandbox):
        return
    
    def before_hid_send(self, sandbox):
        return
        
    def after_hid_send(self, sandbox):
        return



import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB

# ---------------- Layers ----------------
L_NORMAL   = 0
L_GAMING   = 1
L_PREMIERE = 2
L_FN       = 3

# ---------------- Macros ----------------
macros = Macros()

WIN_SHIFT_S = KC.MACRO(
    Press(KC.LGUI),
    Press(KC.LSFT),
    Tap(KC.S),
    Release(KC.LSFT),
    Release(KC.LGUI),
)

TASK_MANAGER = KC.MACRO(
    Press(KC.LCTL),
    Press(KC.LSFT),
    Tap(KC.ESC),
    Release(KC.LSFT),
    Release(KC.LCTL),
)

LOCK_PC = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.L),
    Release(KC.LGUI),
)

CTRL_SHIFT_M = KC.MACRO(
    Press(KC.LCTL),
    Press(KC.LSFT),
    Tap(KC.M),
    Release(KC.LSFT),
    Release(KC.LCTL),
)

CTRL_SHIFT_D = KC.MACRO(
    Press(KC.LCTL),
    Press(KC.LSFT),
    Tap(KC.D),
    Release(KC.LSFT),
    Release(KC.LCTL),
)

ALT_F10 = KC.MACRO(
    Press(KC.LALT),
    Tap(KC.F10),
    Release(KC.LALT),
)

CTRL_K = KC.MACRO(
    Press(KC.LCTL),
    Tap(KC.K),
    Release(KC.LCTL),
)

SHIFT_DELETE = KC.MACRO(
    Press(KC.LSFT),
    Tap(KC.DEL),
    Release(KC.LSFT),
)

CTRL_Z = KC.MACRO(
    Press(KC.LCTL),
    Tap(KC.Z),
    Release(KC.LCTL),
)

CTRL_SHIFT_Z = KC.MACRO(
    Press(KC.LCTL),
    Press(KC.LSFT),
    Tap(KC.Z),
    Release(KC.LSFT),
    Release(KC.LCTL),
)

# ---------------- Keyboard Setup ----------------
keyboard = KMKKeyboard()
keyboard.modules.append(macros)
keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

rgb = RGB(pixel_pin=board.D4, num_pixels=5, animation_mode=AnimationModes.RAINBOW, val_default=30)
keyboard.extensions.append(rgb)

# 3 one-color LEDs
led_blue = digitalio.DigitalInOut(board.LED_BLUE); led_blue.direction = digitalio.Direction.OUTPUT
led_green = digitalio.DigitalInOut(board.LED_GREEN); led_green.direction = digitalio.Direction.OUTPUT
led_red = digitalio.DigitalInOut(board.LED_RED); led_red.direction = digitalio.Direction.OUTPUT

keyboard.extensions.append(LayerLEDs(led_red, led_green, led_blue, active_low=True))
keyboard.extensions.append(BuzzerSounds(board.D5))

# Keys: encoder button is wired as key on D0
PINS = [board.D0, board.D3, board.D6, board.D7, board.D8, board.D9, board.D10]
keyboard.matrix = KeysScanner(pins=PINS, value_when_pressed=False)

# Encoder A/B only; click handled by key on D0
encoder_handler.pins = ((board.D1, board.D2, None, False, 2),)

# ---------------- FN + Button combos for layer switching ----------------
# We implement cycling on FN layer by direct TO() targets:
# FN + Button1 -> Normal, FN + Button2 -> Gaming, FN + Button3 -> Premiere
# (This is robust and avoids needing to track current state.)
FN_TO_NORMAL   = KC.TO(L_NORMAL)
FN_TO_GAMING   = KC.TO(L_GAMING)
FN_TO_PREMIERE = KC.TO(L_PREMIERE)

# ---------------- Encoder click: LT(FN, <tap>) per layer ----------------
ENC_BTN_NORMAL   = KC.LT(L_FN, KC.MUTE)
ENC_BTN_GAMING   = KC.LT(L_FN, CTRL_SHIFT_M)
ENC_BTN_PREMIERE = KC.LT(L_FN, KC.BSLS)  # "\"

# ---------------- Keymaps ----------------
# Order per layer: [ENC_BTN, B1, B2, B3, B4, B5, B6]
keyboard.keymap = [
    # Layer 1: Normal
    [
        ENC_BTN_NORMAL,
        KC.MPLY,      # Play/Pause [web:199]
        KC.MNXT,      # Next [web:199]
        KC.MPRV,      # Prev [web:199]
        WIN_SHIFT_S,  # Win+Shift+S [web:148]
        TASK_MANAGER, # Ctrl+Shift+Esc [web:148]
        LOCK_PC,      # Win+L [web:148]
    ],

    # Layer 2: Gaming
    [
        ENC_BTN_GAMING,
        CTRL_SHIFT_M, # Discord mute toggle
        CTRL_SHIFT_D, # Discord deafen
        ALT_F10,      # Shadowplay instant replay
        KC.F12,       # Steam screenshot
        KC.M,         # Map
        KC.I,         # Inventory
    ],

    # Layer 3: Premiere
    [
        ENC_BTN_PREMIERE,
        CTRL_K,        # Add Edit
        SHIFT_DELETE,  # Ripple delete
        KC.RBRC,    # Zoom In
        KC.SLSH,   # Zoom out (-)
        CTRL_Z,        # Undo
        CTRL_SHIFT_Z,  # Redo
    ],

    # FN layer: layer select + RGB controls (optional)
    [
        KC.TRNS,        # keep LT hold
        FN_TO_NORMAL,   # FN + Button1 -> Normal
        FN_TO_GAMING,   # FN + Button2 -> Gaming
        FN_TO_PREMIERE, # FN + Button3 -> Premiere
        KC.RGB_TOG,          # FN + Button4 -> Static RGB
        KC.RGB_MODE_BREATHE,        # FN + Button5 -> Breathing
        KC.RGB_MODE_RAINBOW,
    ],
]

# ---------------- Encoder rotation per layer ----------------
# tuple: (CCW, CW, Click) and Click is unused because click is on D0 key [web:146]
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.NO),),     # Normal: volume
    ((KC.VOLD, KC.VOLU, KC.NO),),     # Gaming: fallback volume (replace with brightness/discord vol if you add software)
    ((KC.LEFT, KC.RIGHT, KC.NO),),    # Premiere: frame step
    ((KC.NO, KC.NO, KC.NO),),         # FN layer: do nothing
]
print(dir(rgb))
if __name__ == '__main__':
    keyboard.go()
