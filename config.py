from animations.neurons import Pulse
from animations.sound_visualizer import SoundVisualizer

# The number of LEDs per strip
N_LEDS = 150
# The total number of strips plugged into the beaglebone
N_STRIPS = 25

SERVER = '127.0.0.1:7890'

ANIMATIONS = [
    {
        'animation': Pulse,
        'options': {
            # speed is expressed in seconds
            'speed': 1/20.0
        },
        'strip': 24
    },
    {
        'animation': Pulse,
        'options': {
            # speed is expressed in seconds
            'speed': 1/30.0
        },
        'strip': 24
    },
    {
        'animation': Pulse,
        'options': {
            # speed is expressed in seconds
            'speed': 1/25.0
        },
        'strip': 24
    },
    {
        'animation': SoundVisualizer,
        'strip': 24
    }
]
