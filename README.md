# Animations and OPC client for Intention

## What is Intention?
Intention is a large scale tensegrity sculpture that represents a eukaryotic (nucleus-bearing) cell. It has an intricate network of rope (actin filaments) and a nucleus that is the geometric DNA of the outer structure. It is mapped with lighting to respond to sensory input. We are pleased to announce that we are recipients of the Black Rock City Honorarium Grant for 2016!

Down through the cellular level, we are held together by tension and compression, pure efficiency in nature. Intention is a sculpture that explores the connection between the human body and tensegrity structures. We are building an immersive and interactive tensegrity structure representing the biomechanics of a human cell as pioneered by researcher Donald Ingber  that treads the intersections of art, engineering, and science.

## What is this?

This is a threaded library written for driving any OPC (open-pixel-control), as well as a few animations.  As the burn gets closer, there will be more animations for various sensors, but as it stands, there's a sound visualizer, and simple pulses that travel through the wires like blue and green stained actin microfilament

## How did you build this?
With lots of help!  The opc client is based off of [@zestyping's opc client](https://github.com/zestyping/openpixelcontrol), and the sound visualizer is based on [a program that uses matplotlib to display a frequency graph](http://blog.yjl.im/2012/11/frequency-spectrum-of-sound-using.html).  The rest of the code is original.  If you want to create animations, or contribute, feel free too!

We used a beaglebone, LEDscape, and the disorient microcontroller to drive many LED strips at once.  The opc client is written to assume you're using the same setup.

[Learn more about intention!](https://www.indiegogo.com/projects/intention-burning-man-2016-art)

##How to run the software
1. Copy the files to the Beaglebone
2. Run ```python run_animations.py``` in the Terminal
3. Make sure the USB mic is plugged in, otherwise software maybe will not run!