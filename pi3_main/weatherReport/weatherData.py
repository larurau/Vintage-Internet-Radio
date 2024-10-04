import asyncio
import datetime
import json
import subprocess
import os
import edge_tts

TEMP_HIGH_WARNING = 35
TEMP_LOW_WARNING = 0
UV_INDEX_WARNING = 5
WIND_SPEED_WARNING = 30
WIND_GUSTS_WARNING = 48
DAILY_HOURS_OF_SUN_WARNING = 10
SHOW_UV = 2.5
UV_INDEX_HIGH = 5
PRECIP_WARNING = 10
SNOW_WARNING = 2.5
EXTREME_PRECIP_WARNING = 20
EXTREME_SNOW_WARNING = 7.5

# Helper

def weather_code_to_text(code):
    # WMO Weather Interpretation Codes
    weather_code_dict = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle of Light intensity",
        53: "Drizzle of Moderate intensity",
        55: "Drizzle of Dense intensity",
        56: "Freezing Drizzle of Light intensity",
        57: "Freezing Drizzle of Dense intensity",
        61: "Rain of Slight intensity",
        63: "Rain of Moderate intensity",
        65: "Rain of Heavy intensity",
        66: "Freezing Rain of Light intensity",
        67: "Freezing Rain of Heavy intensity",
        71: "Snow fall of Slight intensity",
        73: "Snow fall of Moderate intensity",
        75: "Snow fall of Heavy intensity",
        77: "Snow grains",
        80: "Rain showers of Slight intensity",
        81: "Rain showers of Moderate intensity",
        82: "Rain showers of Violent intensity",
        85: "Snow showers of Slight intensity",
        86: "Snow showers of Heavy intensity",
        95: "Thunderstorm of Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    error_message = f"Error: Invalid weather code {code}, does not match any known weather."
    return weather_code_dict.get(code, )

def degrees_to_cardinal(degree):
    if degree is None:
        return "unknown direction"

    directions = ['North', 'North-Northeast', 'Northeast', 'East-Northeast', 'East',
                  'East-Southeast', 'Southeast', 'South-Southeast', 'South',
                  'South-Southwest', 'Southwest', 'West-Southwest', 'West',
                  'West-Northwest', 'Northwest', 'North-Northwest']

    index = round(degree / 22.5) % 16
    return directions[index]

# Main

def get_weather(lat, long):

    lat_long = f"?latitude={lat}&longitude={long}"
    current = ("&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,"
               "snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,"
               "wind_gusts_10m")
    daily = ("&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,"
             "apparent_temperature_min,sunrise,sunset,daylight_duration,sunshine_duration,uv_index_max,"
             "uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,"
             "precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,"
             "shortwave_radiation_sum,et0_fao_evapotranspiration")
    timezone = "&timezone=Europe/Berlin"
    duration = "&forecast_days=2"

    parameter_string = lat_long + current + daily + timezone + duration

    base_url = "https://api.open-meteo.com/v1/forecast"
    params = parameter_string
    url = base_url + params

    # Execute curl request
    result = subprocess.run(["curl", "-X", "GET", url], capture_output=True, text=True)

    # Parse the response to JSON
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        print("Error with curl request")
        return None

def weather_info_to_text(data, location_name):
    def generate_sun_text(sun_rise, sun_set):

        sunrise_time = datetime.datetime.fromisoformat(sun_rise)
        sunset_time = datetime.datetime.fromisoformat(sun_set)

        # Get the current time
        now = datetime.datetime.now()

        # Determine the correct tense for sunrise
        if now < sunrise_time:
            sunrise_text = f"Sunrise will be at {sunrise_time.strftime('%I:%M %p')}."
        elif now > sunrise_time and (now - sunrise_time).seconds < 3600:
            sunrise_text = f"Sunrise is happening now at {sunrise_time.strftime('%I:%M %p')}."
        else:
            sunrise_text = f"Sunrise was at {sunrise_time.strftime('%I:%M %p')}."

        # Determine the correct tense for sunset
        if now < sunset_time:
            sunset_text = f"Sunset will be at {sunset_time.strftime('%I:%M %p')}."
        elif now > sunset_time and (now - sunset_time).seconds < 3600:
            sunset_text = f"Sunset is happening now at {sunset_time.strftime('%I:%M %p')}."
        else:
            sunset_text = f"Sunset was at {sunset_time.strftime('%I:%M %p')}."

        # Combine the sunrise and sunset text
        return f"{sunrise_text}\n{sunset_text}"

    ##########################################################
    ####################### current ##########################

    # Extract current weather information
    current_weather = data['current']

    current_temperature_2m = current_weather['temperature_2m']
    current_is_day = current_weather['is_day']
    current_weather_code = current_weather['weather_code']
    current_apparent_temperature = current_weather['apparent_temperature']
    current_relative_humidity_2m = current_weather['relative_humidity_2m']
    current_wind_speed_10m = current_weather['wind_speed_10m']
    current_wind_gusts_10m = current_weather['wind_gusts_10m']
    current_wind_direction_10m = current_weather['wind_direction_10m']

    # Current weather text
    text_lines = []
    text_lines.append(f"Current conditions in {location_name}:")
    day_night_value = "Daytime" if current_is_day == 1 else "Nighttime"
    text_lines.append(f"It is currently {day_night_value}.")
    text_lines.append(f"The weather is {weather_code_to_text(current_weather_code)}.")
    if (current_temperature_2m > TEMP_HIGH_WARNING or current_temperature_2m < TEMP_LOW_WARNING
            or current_apparent_temperature > TEMP_HIGH_WARNING or current_apparent_temperature < TEMP_LOW_WARNING):
        text_lines.append(f"Warning: ")
    text_lines.append((f"The temperature is {int(current_temperature_2m)} degrees, and feels like "
             f"{int(current_apparent_temperature)} degrees."))
    text_lines.append(f"The relative humidity is at {int(current_relative_humidity_2m)} %.")
    if current_wind_speed_10m > WIND_SPEED_WARNING or current_wind_gusts_10m > WIND_GUSTS_WARNING:
        text_lines.append(f"Warning: ")
    text_lines.append(f"The wind speed is currently {int(current_wind_speed_10m)} km/h "
             f"coming from {degrees_to_cardinal(current_wind_direction_10m)}, "
             f"with gusts of up to {int(current_wind_gusts_10m)} km/h. \n")

    ##########################################################
    ####################### today ##########################

    # Extract daily weather information
    daily_weather = data['daily']
    daily_weather_code = daily_weather['weather_code']
    daily_temperature_2m_max = daily_weather['temperature_2m_max']
    daily_temperature_2m_min = daily_weather['temperature_2m_min']
    daily_apparent_temperature_max = daily_weather['apparent_temperature_max']
    daily_apparent_temperature_min = daily_weather['apparent_temperature_min']
    daily_sunrise = daily_weather['sunrise']
    daily_sunset = daily_weather['sunset']
    daily_daylight_duration = daily_weather['daylight_duration']
    daily_sunshine_duration = daily_weather['sunshine_duration']
    daily_uv_index_max = daily_weather['uv_index_max']
    daily_uv_index_clear_sky_max = daily_weather['uv_index_clear_sky_max']
    daily_precipitation_sum = daily_weather['precipitation_sum']
    daily_snowfall_sum = daily_weather['snowfall_sum']
    daily_wind_speed_10m_max = daily_weather['wind_speed_10m_max']
    daily_wind_gusts_10m_max = daily_weather['wind_gusts_10m_max']
    daily_wind_direction_10m_dominant = daily_weather['wind_direction_10m_dominant']

    text_lines.append(f"Today's Weather forecast for {location_name}:")
    text_lines.append(f"The weather will be {weather_code_to_text(daily_weather_code[0])}.")

    text_lines.append(generate_sun_text(daily_sunrise[0], daily_sunset[0]))

    text_lines.append((f"Today has {int(daily_daylight_duration[0] / 60 / 60)} hours of daylight with "
                       f"{int(daily_sunshine_duration[0] / 60 / 60)} hours of sunshine."))

    if int(daily_daylight_duration[0] / 60 / 60) < DAILY_HOURS_OF_SUN_WARNING:
        text_lines.append(f"Consider taking vitamin D to help against seasonal mood swings.")

    if int(daily_uv_index_clear_sky_max[0]) > SHOW_UV:
        text_lines.append(
            f"The maximum daily UV index is {daily_uv_index_max[0]} with up to {daily_uv_index_clear_sky_max[0]} under "
            f"clear skies.")

        if int(daily_uv_index_max[0]) > UV_INDEX_HIGH or (int(daily_uv_index_clear_sky_max[0]) > UV_INDEX_HIGH + 1):
            text_lines.append(f"Consider wearing sun screen and a hat to protect against the sun.")

    if (daily_temperature_2m_max[0] > TEMP_HIGH_WARNING or daily_temperature_2m_min[0] < TEMP_LOW_WARNING
            or daily_apparent_temperature_max[0] > TEMP_HIGH_WARNING or daily_apparent_temperature_min[
                0] < TEMP_LOW_WARNING):
        text_lines.append(f"Warning: ")
    text_lines.append(
        f"The temperature will range from {int(daily_temperature_2m_min[0])} to {int(daily_temperature_2m_max[0])}"
        f" degrees. It will feel like {int(daily_apparent_temperature_min[0])} to "
        f"{int(daily_apparent_temperature_max[0])} degrees.")

    if daily_wind_speed_10m_max[0] > WIND_SPEED_WARNING or daily_wind_gusts_10m_max[0] > WIND_GUSTS_WARNING:
        text_lines.append(f"Warning: ")
    text_lines.append(f"The wind speed will be up to {int(daily_wind_speed_10m_max[0])} km/h"
                      f" coming dominantly from {degrees_to_cardinal(daily_wind_direction_10m_dominant[0])}, "
                      f"with gusts of up to {int(daily_wind_gusts_10m_max[0])} km/h.")

    if daily_precipitation_sum[0] > 0:
        if daily_precipitation_sum[0] > EXTREME_PRECIP_WARNING:
            text_lines.append("Warning: Extreme rainfall expected. Prepare for possible flooding.")
        elif daily_precipitation_sum[0] > PRECIP_WARNING:
            text_lines.append("Warning: Heavy rainfall expected. Be cautious of water accumulation.")
        text_lines.append(f"The total precipitation is expected to be {daily_precipitation_sum[0]} mm.")

    # Snowfall check
    if daily_snowfall_sum[0] > 0:
        if daily_snowfall_sum[0] > EXTREME_SNOW_WARNING:
            text_lines.append("Warning: Heavy snowfall expected. Roads may become hazardous.")
        elif daily_snowfall_sum[0] > SNOW_WARNING:
            text_lines.append("Warning: Moderate snowfall expected. Be prepared for travel disruptions.")
        text_lines.append(f"The total snowfall is expected to be {daily_snowfall_sum[0]} mm.")
    text_lines.append("")

    ##########################################################
    ###################### tomorrow ##########################

    text_lines.append(f"Tomorrow's Weather forecast for {location_name}:")
    text_lines.append(f"The weather will be {weather_code_to_text(daily_weather_code[1])}.")

    # Use the sunrise and sunset for tomorrow (index 1)
    text_lines.append(generate_sun_text(daily_sunrise[1], daily_sunset[1]))

    text_lines.append((f"Tomorrow will have {int(daily_daylight_duration[1] / 60 / 60)} hours of daylight with "
                       f"{int(daily_sunshine_duration[1] / 60 / 60)} hours of sunshine."))

    if int(daily_daylight_duration[1] / 60 / 60) < DAILY_HOURS_OF_SUN_WARNING:
        text_lines.append(f"Consider taking vitamin D to help against seasonal mood swings.")

    # UV Index check for tomorrow
    if int(daily_uv_index_clear_sky_max[1]) > SHOW_UV:
        text_lines.append(
            f"The maximum daily UV index is {daily_uv_index_max[1]} with up to {daily_uv_index_clear_sky_max[1]} under "
            f"clear skies.")

        if int(daily_uv_index_max[1]) > UV_INDEX_HIGH or (int(daily_uv_index_clear_sky_max[1]) > UV_INDEX_HIGH + 1):
            text_lines.append(f"Consider wearing sun screen and a hat to protect against the sun.")

    # Temperature warnings for tomorrow
    if (daily_temperature_2m_max[1] > TEMP_HIGH_WARNING or daily_temperature_2m_min[1] < TEMP_LOW_WARNING
            or daily_apparent_temperature_max[1] > TEMP_HIGH_WARNING or daily_apparent_temperature_min[
                1] < TEMP_LOW_WARNING):
        text_lines.append(f"Warning: ")
    text_lines.append(
        f"The temperature will range from {int(daily_temperature_2m_min[1])} to {int(daily_temperature_2m_max[1])}"
        f" degrees. It will feel like {int(daily_apparent_temperature_min[1])} to "
        f"{int(daily_apparent_temperature_max[1])} degrees.")

    # Wind warnings for tomorrow
    if daily_wind_speed_10m_max[1] > WIND_SPEED_WARNING or daily_wind_gusts_10m_max[1] > WIND_GUSTS_WARNING:
        text_lines.append(f"Warning: ")
    text_lines.append(f"The wind speed will be up to {int(daily_wind_speed_10m_max[1])} km/h"
                      f" coming dominantly from {degrees_to_cardinal(daily_wind_direction_10m_dominant[1])}, "
                      f"with gusts of up to {int(daily_wind_gusts_10m_max[1])} km/h.")

    # Precipitation warnings for tomorrow
    if daily_precipitation_sum[1] > 0:
        if daily_precipitation_sum[1] > EXTREME_PRECIP_WARNING:
            text_lines.append("Warning: Extreme rainfall expected. Prepare for possible flooding.")
        elif daily_precipitation_sum[1] > PRECIP_WARNING:
            text_lines.append("Warning: Heavy rainfall expected. Be cautious of water accumulation.")
        text_lines.append(f"The total precipitation is expected to be {daily_precipitation_sum[1]} mm.")

    # Snowfall check for tomorrow
    if daily_snowfall_sum[1] > 0:
        if daily_snowfall_sum[1] > EXTREME_SNOW_WARNING:
            text_lines.append("Warning: Heavy snowfall expected. Roads may become hazardous.")
        elif daily_snowfall_sum[1] > SNOW_WARNING:
            text_lines.append("Warning: Moderate snowfall expected. Be prepared for travel disruptions.")
        text_lines.append(f"The total snowfall is expected to be {daily_snowfall_sum[1]} mm.")
    text_lines.append("\n")

    ##########################################################
    ###################### other info ########################
    text = "\n".join(text_lines)
    return text


async def run_engine(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(output_file)

def text_to_audio(text, chosen_voice = "en-US-AriaNeural"):

    #chosen_voice = "en-US-AriaNeural"
    #chosen_voice = "en-CA-ClaraNeural"
    #chosen_voice = "en-CA-LiamNeural"
    #chosen_voice = "en-US-ChristopherNeural"
    #chosen_voice = "en-US-JennyNeural"

    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, f'resources/weather_report.mp3')

    print("Start TTS...")

    asyncio.run(run_engine(text, chosen_voice, file_path))

    if os.path.exists(file_path):
        print(f"File saved successfully at {file_path}")
    else:
        print("File was not saved")

    return file_path