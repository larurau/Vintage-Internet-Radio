import time

from pi3_main.weatherReport.audioAdjustment import audio_effect
from pi3_main.weatherReport.weatherData import get_weather, weather_info_to_text, text_to_audio

def generate_weather_channel(lat, long, location, voice):

    start_time = time.time()

    weather_data = get_weather(lat=lat, long=long)
    print(weather_data)
    weather_text = weather_info_to_text(weather_data, location)
    print(weather_text)
    file_location = text_to_audio(weather_text, voice)
    audio_effect(file_location)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken: {duration} seconds")