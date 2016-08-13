import opc
from time import sleep
from animations.neurons import Pulse
from animations.sound_visualizer import SoundVisualizer

N_LEDS = 150
N_STRIPS = 25
client = opc.Client('127.0.0.1:7890', N_STRIPS, N_LEDS)

results = {}

def flush(strip_no):
    while True:
        frame = [(0, 0, 0) for result in xrange(N_LEDS)]
        for animation in results.itervalues():
            for led, (r, g, b) in animation.iteritems():
                frame[led] = (
                    frame[led][0] + r,
                    frame[led][1] + g,
                    frame[led][2] + b
                )
        client.put_pixels(strip_no, frame)
        sleep(1.0/50.0) # 50 fps seems like a good amount

results['pulse_1'] = {}
p = Pulse(N_LEDS, results['pulse_1'], speed=1/20.0, color=(0, 100, 0))
p.start()
results['pulse_2'] = {}
p = Pulse(N_LEDS, results['pulse_2'], speed=1/30.0, color=(0, 100, 0))
p.start()
results['pulse_3'] = {}
p = Pulse(N_LEDS, results['pulse_3'], speed=1/25.0, color=(0, 100, 0))
p.start()
results['sound_visualizer'] = {}
sv = SoundVisualizer(N_LEDS, results['sound_visualizer'])
sv.start()

while True:
    flush(24)
