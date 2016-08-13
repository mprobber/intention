import struct
import numpy as np
import pyaudio
from time import sleep
from base_animation import BaseAnimation


nFFT = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

class SoundVisualizer(BaseAnimation):
    def __init__(self, *args, **kwargs):
        super(SoundVisualizer, self).__init__(*args, **kwargs)
        p = pyaudio.PyAudio()
        self.MAX_y = 2.0 ** (p.get_sample_size(FORMAT) * 8 - 1)

        self.colors = kwargs.get('colors') or [255, 255, 255]
        self.color_speed = kwargs.get('color_speed') or [8, 16, 32]

        self.stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=1 * nFFT
        )

    def run(self):
        while True:
            # Read n*nFFT frames from stream, n > 0
            N = max(self.stream.get_read_available() / nFFT, 1) * nFFT
            data = self.stream.read(N, exception_on_overflow=False)
            if not data:
                continue

            # Unpack data, LRLRLR...
            y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / self.MAX_y
            y_L = y[::2]
            y_R = y[1::2]

            Y_L = np.fft.fft(y_L, nFFT)
            Y_R = np.fft.fft(y_R, nFFT)

            # Sewing FFT of two channels together, DC part uses right channel's
            Y = abs(np.hstack((Y_L[-nFFT / 2:-1], Y_R[:nFFT / 2])))

            for m, i in enumerate(np.arange(0, len(Y), len(Y)/float(self.n_leds))):
                level = (Y[int(i)]/10.0)
                self.strip[m] = (
                    int(self.colors[0]*level),
                    int(level*self.colors[1]),
                    int(level*self.colors[2])
                )

                for i, color in enumerate(self.colors):
                    if self.color_speed[i] + color >= 256 or self.color_speed[i] + color <= 0:
                        self.color_speed[i] = -self.color_speed[i]
                    self.colors[i] += self.color_speed[i]
            sleep(1/200.0)
