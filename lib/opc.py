#!/usr/bin/env python

"""Python Client library for Open Pixel Control
http://github.com/zestyping/openpixelcontrol

Sends pixel values to an Open Pixel Control server to be displayed.
http://openpixelcontrol.org/

Recommended use:

    import opc

    # Create a client object
    client = opc.Client('localhost:7890')

    # Test if it can connect (optional)
    if client.can_connect():
        print 'connected to %s' % ADDRESS
    else:
        # We could exit here, but instead let's just print a warning
        # and then keep trying to send pixels in case the server
        # appears later
        print 'WARNING: could not connect to %s' % ADDRESS

    # Send pixels forever at 30 frames per second
    while True:
        my_pixels = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        if client.put_pixels(my_pixels, channel=0):
            print '...'
        else:
            print 'not connected'
        time.sleep(1/30.0)

"""

from time import sleep
import socket
import numpy as np

class Client(object):

    def __init__(self, server_ip_port, strips, leds_per_strip, long_connection=True, verbose=False):
        """Create an OPC client object which sends pixels to an OPC server.

        server_ip_port should be an ip:port or hostname:port as a single string.
        For example: '127.0.0.1:7890' or 'localhost:7890'

        strips:  The number of strips connected to your beaglebone

        leds_per_strip: the number of LEDs on each strip

        There are two connection modes:
        * In long connection mode, we try to maintain a single long-lived
          connection to the server.  If that connection is lost we will try to
          create a new one whenever put_pixels is called.  This mode is best
          when there's high latency or very high framerates.
        * In short connection mode, we open a connection when it's needed and
          close it immediately after.  This means creating a connection for each
          call to put_pixels. Keeping the connection usually closed makes it
          possible for others to also connect to the server.

        A connection is not established during __init__.  To check if a
        connection will succeed, use can_connect().

        If verbose is True, the client will print debugging info to the console.

        """

        self.testStripId = 5

        self.verbose = verbose

        self._long_connection = long_connection

        self._ip, self._port = server_ip_port.split(':')
        self._port = int(self._port)

        self._socket = None  # will be None when we're not connected

	self._light_strips = np.zeros((strips, leds_per_strip, 3), dtype=np.uint8)

    def _debug(self, m):
        if self.verbose:
            print('    %s' % str(m))

    def _ensure_connected(self):
        """Set up a connection if one doesn't already exist.

        Return True on success or False on failure.

        """
        if self._socket:
            self._debug('_ensure_connected: already connected, doing nothing')
            return True

        try:
            self._debug('_ensure_connected: trying to connect...')
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(1)
            self._socket.connect((self._ip, self._port))
            self._debug('_ensure_connected:    ...success')
            return True
        except socket.error:
            self._debug('_ensure_connected:    ...failure')
            self._socket = None
            return False

    def disconnect(self):
        """Drop the connection to the server, if there is one."""
        self._debug('disconnecting')
        if self._socket:
            self._socket.close()
        self._socket = None

    def can_connect(self):
        """Try to connect to the server.

        Return True on success or False on failure.

        If in long connection mode, this connection will be kept and re-used for
        subsequent put_pixels calls.

        """
        success = self._ensure_connected()
        if not self._long_connection:
            self.disconnect()
        return success

    def put_pixels(self, strip, pixels):
        """Send the list of pixel colors to the OPC server on the given channel.

        strip: Which strand of lights to send the pixel colors to.

        pixels: A list of 3-tuples representing rgb colors.
            Each value in the tuple should be in the range 0-255 inclusive. 
            For example: [(255, 255, 255), (0, 0, 0), (127, 0, 0)]
            Floats will be rounded down to integers.
            Values outside the legal range will be clamped.

        Will establish a connection to the server as needed.

        On successful transmission of pixels, return True.
        On failure (bad connection), return False.

        The list of pixel colors will be applied to the LED string starting
        with the first LED.  It's not possible to send a color just to one
        LED at a time (unless it's the first one).

        """
	result = []
        for i, (r, g, b) in enumerate(pixels):
	   result.append((min(255, max(0, int(r))), min(255, max(0, int(g))), min(255, max(0, int(b)))))

	# results are 10, 12, 24
        # ********************************************************************************************************************************************
	# **************************THIS IS WHERE THE STRIPS ARE DEFINED!!!
	# ******************************************************************************************************************************************** 

       # LED test stript to find the right output numbers
       # self.testStripId = 11
       # self._light_strips[self.testStripId] = np.array(result)
       # print "strip #"
       # print self.testStripId
       # print '/n'
       # sleep(1)
       # self.testStripId += 1
       # return self._put_pixels_np(self._light_strips)

        
        self._light_strips[10] = np.array(result)
        
        #output 12 goes to strip 5
        self._light_strips[12] = np.array(result)
        
        #output 24
        self._light_strips[24] = np.array(result)
        
        #the fourth output 11, plugged into strip 6 
        self._light_strips[11] = np.array(result)

        return self._put_pixels_np(self._light_strips)

    def _put_pixels_np(self, pixels, channel=0):
        """
        Sends a numpy array as an OPC command on a given channel,

        pixels: a numpy array of pixels for each strip connected

        channel: what cahnnel to send the pixels on.  for LEDscape, it's always 0
        """
        self._debug('put_pixels: connecting')
        is_connected = self._ensure_connected()
        if not is_connected:
            self._debug('put_pixels: not connected.  ignoring these pixels.')
            return False

        # build OPC message
        len_hi_byte = int((len(pixels)*len(pixels[0]))*3 / 256)
        len_lo_byte = ((len(pixels)*len(pixels[0]))*3) % 256
        bytestr = chr(channel) + chr(0) + chr(len_hi_byte) + chr(len_lo_byte)
	bytestr += str(bytearray(pixels.data))
        self._debug('put_pixels: sending pixels to server')
        try:
            self._socket.send(bytestr)
        except socket.error:
            self._debug('put_pixels: connection lost.  could not send pixels.')
            self._socket = None
            return False

        if not self._long_connection:
            self._debug('put_pixels: disconnecting')
            self.disconnect()

        return True
