import os

from pydub import AudioSegment
import numpy
from scipy.signal import butter, lfilter
from pydub.generators import WhiteNoise, Sine, Square

def __apply_radio_eq(audio, low_cut=200, high_cut=4000):
    order = 5
    audio = audio.set_channels(1)
    nyquist = 0.5 * audio.frame_rate
    low = low_cut / nyquist
    high = high_cut / nyquist

    b, a = butter(order, [low, high], btype='band')
    filtered_audio = lfilter(b, a, audio.get_array_of_samples())
    return audio._spawn(filtered_audio.astype(numpy.int16))

def __apply_low_bit_depth(audio, bit_depth=8, sample_rate=10000):
    processed_audio = audio.set_sample_width(bit_depth // 8)
    processed_audio = processed_audio.set_frame_rate(sample_rate)
    return processed_audio

def __add_radio_noise(audio, base_noise_level=-19.0, harmonic_noise_level=-29.0, white_noise_level=-70.0, base_freq=50,
                      harmonic_freq=50):

    duration_ms = len(audio)

    base_hum = Sine(base_freq).to_audio_segment(duration=duration_ms).apply_gain(base_noise_level)
    harmonic_buzz = Square(harmonic_freq).to_audio_segment(duration=duration_ms).apply_gain(harmonic_noise_level)
    white_noise = WhiteNoise().to_audio_segment(duration=duration_ms)

    base_hum = base_hum - (audio.dBFS - base_noise_level)
    harmonic_buzz = harmonic_buzz - (audio.dBFS - harmonic_noise_level)
    white_noise = white_noise - (audio.dBFS - white_noise_level)

    noisy_audio = audio.overlay(base_hum).overlay(harmonic_buzz).overlay(white_noise)

    return noisy_audio

def audio_effect(file_path):

    audio = AudioSegment.from_mp3(file_path)
    print("Apply eq ...")
    audio = __apply_radio_eq(audio)
    print("Apply bit depth ...")
    audio = __apply_low_bit_depth(audio)
    print("Apply noise ...")
    audio = __add_radio_noise(audio)

    # Export processed audio with effects
    current_directory = os.getcwd()
    output_path = os.path.join(current_directory, f'resources/weather_report_with_radio_effects.mp3')
    audio.export(output_path, format="mp3")
