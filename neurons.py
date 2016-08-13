import opc
import random
from time import sleep
from threading import Thread
import signal

client = opc.Client('127.0.0.1:7890', 25, 150)

n_pulses = 5
n_leds = 150

len_tails = 8

results = [(0, 0, 0) for i in xrange(n_leds)]
running = True

results = {}

class Pulse(object):
    def __init__(self, speed, color, location):
        self.speed = speed
        self.color = color
        self.location = location
        self.t = Thread(target = self._run_pulse)
        self.t.daemon = True
        self.t.start()

    def _run_pulse(self):
        while running:
            r, g, b = self.color
            results[id(self)] = {}
            my_results = results[id(self)]
            my_results[(self.location - len_tails) % n_leds] = (0, 0, 0)
            for tail in xrange(len_tails):
                my_index = (self.location - tail) % n_leds
                my_results[my_index] = \
                    (r, g, b)
                r = r / 1.5
                g = g / 1.5
                b = b / 1.5
            self.location = (self.location + 1) % n_leds
            sleep(self.speed)


def flushing_thread():
    while running:
        my_results = [(0, 0, 0) for result in xrange(n_leds)]
        for thread in results.itervalues():
            for led_number, (r, g, b) in thread.iteritems():
                my_results[led_number] = (
                    my_results[led_number][0] + r,
                    my_results[led_number][1] + g,
                    my_results[led_number][2] + b
                )
        client.put_pixels(24, my_results)
        sleep(1.0/100.0)

p = Pulse(1.0/20.0, (0, 100, 0), 8)
flush = Thread(target=flushing_thread)
flush.daemon = True
flush.start()

while True:
    signal.pause()
