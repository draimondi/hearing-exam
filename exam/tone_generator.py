"""
Class for running a thread which produces a Tone.
The tone can be changed in frequency and volume on the fly

Contains:
    - ToneThread
"""
import threading
import time
import numpy as np
import pyaudio

class ToneThread(threading.Thread):
    """This class instantiates a thread which, when run, plays a sine wave audio tone."""
    BOTH_CHANNELS = "both"
    LEFT_CHANNEL = "left"
    RIGHT_CHANNEL = "right"
    BITS = 16
    TONE_ARRAY_TYPE = np.float32
    DEFAULT_SAMPLE_RATE =  44100 # sample rate: frames/samples per second. Hz, must be integer
    DEFAULT_FREQUENCY = 440.0 # sine frequency, Hz, may be float
    DEFAULT_PERIOD = 0.2 # in seconds, may be float
    DEFAULT_LOOPS = 1 # number of times to play the tone. -1 for infinite

    def generate_sine_wave(self, num_samples, array_type):
        """Generates a sine wave array of the specified type"""
        sample_array = np.arange(num_samples, dtype=array_type) #creates a template array
        sine_array = np.sin(2*np.pi*sample_array*
            self.frequency/self.sample_rate) #applies sine wave pattern to the array
        return sine_array

    def make_stereo_tone(self):
        """Generates a stereo tone compatible with pyaudio"""
        num_samples = int(round(self.duration*self.sample_rate))    # Sample count
        audio_wave =  self.generate_sine_wave(num_samples, self.TONE_ARRAY_TYPE)
        empty_wave = np.zeros(shape=num_samples, dtype=self.TONE_ARRAY_TYPE)
        left_wave = (audio_wave if self.channel in (self.LEFT_CHANNEL , self.BOTH_CHANNELS)
            else empty_wave)
        right_wave = (audio_wave if self.channel in (self.RIGHT_CHANNEL , self.BOTH_CHANNELS)
            else empty_wave)
        self.tone = np.ravel([left_wave,right_wave],'F')
        
    def generate_sine_tone(self):
        """Generates an array that contains values mathing a sine wave"""
        sample_time=1.0/self.sample_rate
        num_samples = self.sample_rate*self.duration    # Sample count
        time_vector = np.arange(num_samples) * sample_time # Time vector
        #Define the highest value for each sample
        max_sample = 2**(self.BITS - 1) - 1
        signal = max_sample *self.volume*np.sin(2*np.pi * self.frequency*time_vector)
        return signal

    def __init__(self, frequency=DEFAULT_FREQUENCY,
                 rate=DEFAULT_SAMPLE_RATE, period=DEFAULT_PERIOD,
                 loops=DEFAULT_LOOPS, sleep_between_loops=False):
        super().__init__()
        self.tone = None                    # The array representing the audio tone
        self.frequency = frequency          # frequency in Hz, may be float
        self.sample_rate = rate             # sampling rate in Hz, must be integer
        self.duration = period              # in seconds, may be float
        self.volume = 1.0                   # Volume of the tone. Float, between 0 and 1
        self.stopped = False                # Stop playing the tone
        self.channel = self.BOTH_CHANNELS   # The speaker on which to play the tone.
        self.loops = loops                  # Number of times to play the tone. -1 means infinite
        self.sleep_between_loops=sleep_between_loops      # Include a pause between tone loops
        self.graph = None
        self.make_stereo_tone()
        self.stream = pyaudio.PyAudio().open(
            format = pyaudio.paFloat32, channels = 2, rate = self.sample_rate, output = True)

    def get_duration(self):
        """Returns the duration of the generated tone"""
        return self.duration

    def get_volume(self):
        """Returns the current volume of the generated tone"""
        return self.volume

    def set_volume(self, volume):
        """Sets the volume of the generated tone"""
        self.volume = volume

    def set_frequency(self, hertz):
        """Sets the frequency of the generated tone"""
        self.frequency = int(hertz)
        self.make_stereo_tone()

    def mute(self):
        """Mutes the generated tone"""
        self.stopped = True

    def unmute(self):
        """Unmutes the generated tone"""
        self.stopped = False

    def set_channel(self, channel):
        """Sets the channel where to play the generated tone.
           'channel' parameter can be ''left', 'right' or 'both'
        """
        self.channel = channel
        self.make_stereo_tone()

    def run(self):
        """Generates the tone and plays it to the default audio device"""
        loop=0
        while not self.stopped and (loop < self.loops or self.loops == -1):
            self.stream.write((self.tone * self.volume).tobytes())

            if self.loops != -1:
                loop = loop + 1
            if self.sleep_between_loops:
                time.sleep(self.duration*2)
