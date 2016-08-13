from time import sleep
import random
from base_animation import BaseAnimation

class Pulse(BaseAnimation):
    def __init__(self, *args, **kwargs):
        super(Pulse, self).__init__(*args, **kwargs)
        self.speed = kwargs.get('speed') or (1.0/20.0)
        self.color = kwargs.get('color') or (0, 100, 0)
        self.location = kwargs.get('location') or random.randint(0, self.n_leds)

    def run(self):
        while True:
            r, g, b = self.color
            self.strip.clear()
            for tail in xrange(8):
                my_index = (self.location - tail) % self.n_leds
                self.strip[my_index] = (r, g, b)
                r = r / 1.5
                g = g / 1.5
                b = b / 1.5
            self.location = (self.location + 1) % self.n_leds
            sleep(self.speed)
