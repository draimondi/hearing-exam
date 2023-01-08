"""Performs general tests."""
from exam import tone_generator

def test_tone_generator():
    """Test tone generation"""
    sound_thread = tone_generator.ToneThread()
    assert sound_thread.generate_sine_tone() is not None

def test_volume():
    """Checks volume of the tone"""
    sound_thread = tone_generator.ToneThread()
    sound_thread.set_volume(0.75)
    assert sound_thread.volume == 0.75

def test_duration():
    """Checks duration of the tone"""
    sound_thread = tone_generator.ToneThread()
    assert sound_thread.get_duration() == sound_thread.DEFAULT_PERIOD

def test_frequency():
    """Checks volume of the tone"""
    sound_thread = tone_generator.ToneThread()
    sound_thread.set_frequency(6000)
    assert sound_thread.frequency == 6000
