"""Formatting utilities for weather display values.

Provides functions to convert raw API values (WMO weather codes and wind
direction degrees) into human-readable strings.
"""

WMO_WEATHER_CODES = {
    0: "Clear",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail",
}


def format_weather_code(code: int) -> str:
    """Return human-readable text for a WMO weather interpretation code.

    Args:
        code: WMO weather interpretation code from the Open-Meteo API.

    Returns:
        A descriptive weather condition string, or "Unknown (<code>)" if
        the code is not recognized.
    """
    return WMO_WEATHER_CODES.get(code, f"Unknown ({code})")


def format_wind_direction(degrees: int) -> str:
    """Convert wind direction in degrees to a 16-point cardinal label.

    Args:
        degrees: Wind direction in degrees (0–360), where 0/360 is North.

    Returns:
        A cardinal or intercardinal direction string (e.g., "NNE"), or
        "Unknown" if the value is outside the valid range.
    """
    if not 0 <= degrees <= 360:
        return "Unknown"

    directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    index = round(degrees / 22.5) % 16
    return directions[index]
