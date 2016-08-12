import struct
import wave
import sys
import numpy as np
import pyaudio
import random
import opc
from time import sleep

SAVE = 0.0
TITLE = ''
WIDTH = 1280
HEIGHT = 720
FPS = 25.0

nFFT = 512
BUF_SIZE = 1 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

n_LEDs = 150

current_colors = [255, 255, 255]
color_speed = [8, 16, 32]

nPulses = 3

pulse_locations = [random.randint(1, n_LEDs) for i in xrange(nPulses)]
pulse_speeds = [1 for i in xrange(nPulses)]

global client

def animate(stream, MAX_y):

  # Read n*nFFT frames from stream, n > 0
  N = max(stream.get_read_available() / nFFT, 1) * nFFT
  data = stream.read(N, exception_on_overflow=False)
  if not data:
    return

  # Unpack data, LRLRLR...
  y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
  y_L = y[::2]
  y_R = y[1::2]

  Y_L = np.fft.fft(y_L, nFFT)
  Y_R = np.fft.fft(y_R, nFFT)

  # Sewing FFT of two channels together, DC part uses right channel's
  Y = abs(np.hstack((Y_L[-nFFT / 2:-1], Y_R[:nFFT / 2])))

  result = []
  for m, i in enumerate(np.arange(0, len(Y), len(Y)/float(n_LEDs))):
    level = (Y[int(i)]/10.0)
    result.append((int(current_colors[0]*level), int(level*current_colors[1]), int(level*current_colors[2])))
    for i, color in enumerate(current_colors):
        if color_speed[i] + color >= 256 or color_speed[i] + color <= 0:
            color_speed[i] = -color_speed[i]
        current_colors[i] += color_speed[i]
  for i in xrange(n_LEDs):
    if i in pulse_locations:
#       result[i] = (255, 255, 255)
      for i, pulse_location in enumerate(pulse_locations):
        if pulse_location + pulse_speeds[i] == n_LEDs or pulse_location + pulse_speeds[i] == 0:
            pulse_speeds[i] = -pulse_speeds[i]
        pulse_locations[i] += pulse_speeds[i]
  client.put_pixels(24, result)
  sleep(1/200.0)
  return



def main():

  # Frequency range
  p = pyaudio.PyAudio()
  # Used for normalizing signal. If use paFloat32, then it's already -1..1.
  # Because of saving wave, paInt16 will be easier.
  MAX_y = 2.0 ** (p.get_sample_size(FORMAT) * 8 - 1)

  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=BUF_SIZE)
  while True:
    animate(stream, MAX_y)




#-------------------------------------------------------------------------------
# handle command line

if len(sys.argv) == 1:
  IP_PORT = '127.0.0.1:7890'
elif len(sys.argv) == 2 and ':' in sys.argv[1] and not sys.argv[1].startswith('-'):
  IP_PORT = sys.argv[1]
else:
  print('''
Usage: raver_plaid.py [ip:port]

If not set, ip:port defauls to 127.0.0.1:7890
''')
  sys.exit(0)


#-------------------------------------------------------------------------------
# connect to server

client = opc.Client(IP_PORT, 25, 150)
if client.can_connect():
  print('    connected to %s' % IP_PORT)
else:
  # can't connect, but keep running in case the server appears later
  print('    WARNING: could not connect to %s' % IP_PORT)
print('')






main()
