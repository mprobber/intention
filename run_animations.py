from lib import opc
from time import sleep
from threading import Thread
import signal
import config

client = opc.Client(config.SERVER, config.N_STRIPS, config.N_LEDS)

results = {}

def flush(strip_no):
    while True:
        frame = [(0, 0, 0) for result in xrange(config.N_LEDS)]
        for animation in results.itervalues():
            for led, (r, g, b) in animation.iteritems():
                frame[led] = (
                    frame[led][0] + r,
                    frame[led][1] + g,
                    frame[led][2] + b
                )
        client.put_pixels(strip_no, frame)
        sleep(1.0/50.0) # 50 fps seems like a good amount

allStrips = set()

for i, animation in enumerate(config.ANIMATIONS):
    results[i] = {}
    a = animation['animation'](config.N_LEDS, results[i], **(animation.get('options') or {}))
    allStrips.add(animation['strip'])
    a.start()

for strip in allStrips:
    t = Thread(target=flush, args=(strip,))
    t.daemon = True
    t.start()

while True:
    signal.pause()
