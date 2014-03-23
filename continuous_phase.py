# http://stackoverflow.com/questions/3089832/sine-wave-glissando-from-one-pitch-to-another-in-numpy
import sys
import time

from pylab import *
import pygame.mixer
import pygame.sndarray

from scipy.ndimage.filters import gaussian_filter1d

sample_rate = 48000 # Hz
f0, f1 = 1760, 1864 # Hz
t_length = 0.040 # seconds
t_change = 0.020 # seconds
steepness = 1600.0


def _freqs(alphabet, base_freq, multiplier):
    freq = base_freq
    result = {}
    for symbol in alphabet:
        result[symbol] = freq
        freq = int(freq * multiplier)
    return result

freq_table = _freqs('0123456789abcdefghijklmnopqrstuv', 1760, 2**(1/12.0))


chirp = 'hj' 'gfhd9532dm' '4fbeu0mo'
freqs = [freq_table[symbol] for symbol in chirp]


times = arange(0, len(chirp)*87.2e-3, 1./sample_rate)

freq = array([freqs[int(t/87.2e-3)] for t in times])
freq = gaussian_filter1d(freq, 500)
#ramp = array([0.0 if t < t_change else 1.0 for t in times])
#ramp = 1./(1+exp(-steepness*(times-t_change)))
#freq = f0*(1-ramp)+f1*ramp
phase_correction = add.accumulate(times*concatenate((zeros(1), 2*pi*(freq[:-1]-freq[1:]))))

figure()
subplot(311)
plot(times, freq)
subplot(312)
plot(times, 0.5*sin(2*pi*freq*times))
subplot(313)
plot(times, 0.5*sin(2*pi*freq*times+phase_correction))

show()

pygame.mixer.init(sample_rate, -16, 1)
samples = (16384 * 0.5*sin(2*pi*freq*times+phase_correction)).astype(int16)
snd = pygame.sndarray.make_sound(samples)
snd.play()
time.sleep(5)
