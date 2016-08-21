from animations.neurons import Pulse
from animations.color import Color
from animations.sound_visualizer import SoundVisualizer

# The number of LEDs per strip
N_LEDS = 300
# The total number of strips plugged into the beaglebone
N_STRIPS = 32

SERVER = '127.0.0.1:7890'

#STRIP PARAMETER IS NOT BEING USED!!!! for now, strips are hard-coded in lib/opc.py

ANIMATIONS = [
    {
	    'animation': Color,
	    'options': {
               'speed': 1/24.,
	       'color': (100,100,100)
	    },
	    'strip': 0
    },

#    {
#	    'animation': Color,
#	    'options': {
 #              'speed': 1/24.,
#	       'color': (255,255,255)
#	    },
 #	'strip':24
#	}
    
    {
        'animation': Pulse,
        'options': {
            # speed is expressed in seconds
            'speed': 1/20.0,
            'color':(0,255,204)
        },
        'strip': 24
    },

    {
        'animation': SoundVisualizer,
        'strip': 24
    },

    {
        'animation': Pulse,
        'options': {
            # speed is expressed in seconds
            'speed': 1/30.0
       },
        'strip': 13
    },
    {
        'animation': Pulse,
        'options': {
            # speed is expressed in seconds
            'speed': 1/25.0
        },
       'strip': 24
    }
]
