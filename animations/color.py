from time import sleep
import random
from base_animation import BaseAnimation

class Color(BaseAnimation):
    def __init__(self, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.color = kwargs.get('color') or (0, 255, 0)
        self.location = kwargs.get('location') or random.randint(0, self.n_leds)

    def run(self):
        while True:
            r, g, b = self.color
            self.strip.clear()
            for i in xrange(self.n_leds):
                self.strip[i] = self.color
            sleep(0.1)
