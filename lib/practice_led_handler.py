"""
LED hints for the external practice tool (Practice tab).

Mirrors Songs > Learn behaviour:
- one LED per key (no adjacent spill)
- current notes bright, upcoming notes dim
"""

from lib.functions import get_note_position, fastColorWipe
from lib.rpi_drivers import Color

BRIGHTNESS_CURRENT = 0.5
BRIGHTNESS_PREVIEW = 0.05
TIME_BUCKET_SECONDS = 0.06


class PracticeLedHandler:
    def __init__(self, ledstrip, ledsettings, learning):
        self.ledstrip = ledstrip
        self.ledsettings = ledsettings
        self.learning = learning
        # midi_note -> (note_position, channel, song_time)
        self._active_hints = {}

    def clear(self):
        self._active_hints.clear()
        fastColorWipe(self.ledstrip.strip, True, self.ledsettings)

    @staticmethod
    def is_hint_channel(channel):
        return channel in (11, 12)

    def handle_note_on(self, msg):
        channel = getattr(msg, "channel", 0)
        if not self.is_hint_channel(channel):
            return False

        note_position = get_note_position(msg.note, self.ledstrip, self.ledsettings)
        if note_position < 0 or note_position >= self.ledstrip.led_number:
            return True

        song_time = float(getattr(msg, "time", 0) or 0)
        self._active_hints[msg.note] = (note_position, channel, song_time)
        self._render_hints()
        return True

    def handle_note_off(self, msg):
        channel = getattr(msg, "channel", 0)
        if not self.is_hint_channel(channel):
            return False

        self._active_hints.pop(msg.note, None)
        self._render_hints()
        return True

    def _render_hints(self):
        if not self._active_hints:
            fastColorWipe(self.ledstrip.strip, True, self.ledsettings)
            return

        if self.learning.show_future_notes == 1 and len(self._active_hints) > 1:
            current_time = min(entry[2] for entry in self._active_hints.values())
        else:
            current_time = None

        fastColorWipe(self.ledstrip.strip, True, self.ledsettings)

        for _note, (note_position, channel, song_time) in self._active_hints.items():
            if not self._hand_active(channel):
                continue

            is_preview = (
                self.learning.show_future_notes == 1
                and current_time is not None
                and (song_time - current_time) > TIME_BUCKET_SECONDS
            )

            brightness = BRIGHTNESS_PREVIEW if is_preview else BRIGHTNESS_CURRENT
            red, green, blue = self._hand_color(channel, brightness)
            self.ledstrip.strip.setPixelColor(note_position, Color(red, green, blue))

        self.ledstrip.strip.show()

    def _hand_active(self, channel):
        if channel == 12:
            return self.learning.is_led_activeR == 1
        if channel == 11:
            return self.learning.is_led_activeL == 1
        return False

    def _hand_color(self, channel, brightness):
        if channel == 12:
            palette = self.learning.hand_colorList[self.learning.hand_colorR]
        else:
            palette = self.learning.hand_colorList[self.learning.hand_colorL]
        return [int(c * brightness) for c in palette]
