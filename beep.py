#!/usr/bin/env python
"""Minimal implementation of the unix beep command, playing sound with pygame.
"""

import math
import argparse
import time

import numpy
import pygame.mixer
import pygame.sndarray

sample_rate = 44100
sample_size = -16
sample_type = numpy.int16
channels = 1

def sine_sound(freq, duration):
    """Return a `pygame.mixer.Sound` which will play a tone at `freq` Hz for
    `duration` seconds.
    """
    nsamples = int(duration * sample_rate)
    samples = [int(16384 * math.sin(2.0 * math.pi * freq * t / sample_rate))
               for t in xrange(0, nsamples)]
    samples = numpy.array(samples, sample_type)
    return pygame.sndarray.make_sound(samples)

def beep(freq, duration):
    """Play a beep for `duration` seconds at `freq` hertz.

    Blocks whilst playing.
    """ 
    snd = sine_sound(freq, duration)
    snd.play()
    time.sleep(duration)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=float, dest='freq',
                        metavar='N', default=750.0,
                        help="Beep at %(metavar)s Hz [default: %(default)s]")
    parser.add_argument('-l', type=float, dest='duration',
                        metavar='N', default=100.0,
                        help="Beep for %(metavar)s milliseconds "
                             "[default: %(default)s]")
    args = parser.parse_args()

    pygame.mixer.init(sample_rate, sample_size, channels)
    beep(args.freq, args.duration/1000)

if __name__ == '__main__':
    main()
