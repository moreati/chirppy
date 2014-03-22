#!/usr/bin/env python
"""Act as a chirp.io beak, play shortcodes to be decoded by any listening
brains.
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

chirp_symbols = '0123456789abcdefghijklmnopqrstuv'
chirp_base_freq = 1760
note_duration = 87.2e-3
semitone = 2**(1/12.0)


def _freqs(symbols, base_freq, multiplier):
    freq = chirp_base_freq
    result = {}
    for symbol in symbols:
        result[symbol] = freq
        freq = int(freq * multiplier)
    return result

chirp_freqs = _freqs(chirp_symbols, chirp_base_freq, semitone)

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

def chirp(symbols):
    for symbol in symbols:
        beep(chirp_freqs[symbol], note_duration)

def main():
    pygame.mixer.init(sample_rate, sample_size, channels)
    chirp('hj' 'gfhd9532dm' '4fbeu0mo')

if __name__ == '__main__':
    main()
