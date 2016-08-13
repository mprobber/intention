from threading import Thread

class BaseAnimation(object):
    def __init__(self, n_leds, strip, **kwargs):
        self.n_leds = n_leds
        self.strip = strip
        self.t = Thread(target = self.run)
        self.t.daemon = True

    def start(self):
        return self.t.start()

    def run(self):
        raise Exception("You have not defined a run method")
