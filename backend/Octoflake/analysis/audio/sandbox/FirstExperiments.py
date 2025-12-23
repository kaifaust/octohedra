from dataclasses import dataclass

import numpy as np
from playsound import playsound
from scipy.io import wavfile

samplerate = 44100;
fs = 1000
t = np.linspace(0., 1., samplerate)
amplitude = np.iinfo(np.int16).max
data = amplitude * np.sin(2. * np.pi * fs * t)
wavfile.write("example.wav", samplerate, data.astype(np.int16))

playsound('example.wav')


class Riff:
    pass

    def render(self, filename):
        pass



class Line:
    pass

class Hit:
    pass


duration: int = 44100


@dataclass
class Patch:
    pass




class Filter:
    pass


class Envelope:
    pass



class Oscillator:



    def get_sample(self, t):
        pass

class SinWave(Oscillator):

    def get_sample(self, t):
        pass




class SquareWave(Oscillator):



    def get_sample(self, t):
        super().get_sample(t)
