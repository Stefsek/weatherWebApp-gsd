"""Weather data retrieval from the Open-Meteo forecast API."""

import requests
from typing import Optional

from src.weather_app.models.weather_data import WeatherData
from src.weather_app.services.geocoding import GeocodingError, NetworkError


class WeatherAPIError(Exception):
    """Raised when weather API fails."""

    pass


def get_current_weather(
    lat: float, lon: float, location_name: str = "Unknown"
) -> WeatherData:
    """Fetch current weather conditions from the Open-Meteo API.

    Args:
        lat: Geographic latitude in decimal degrees (-90 to 90).
        lon: Geographic longitude in decimal degrees (-180 to 180).
        location_name: Human-readable name attached to the returned data.
            Defaults to "Unknown".

    Returns:
        A WeatherData instance populated with the current conditions.

    Raises:
        WeatherAPIError: If lat/lon are out of range or the API response is
            missing expected fields.
        NetworkError: If the HTTP request fails due to a connectivity issue.
    """
    if not -90 <= lat <= 90:
        raise WeatherAPIError("Latitude must be between -90 and 90")
    if not -180 <= lon <= 180:
        raise WeatherAPIError("Longitude must be between -180 and 180")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m",
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Network error while fetching weather: {e}")

    data = response.json()

    if "current" not in data:
        raise WeatherAPIError("Invalid response from weather API")

    current = data["current"]

    return WeatherData(
        temperature_c=current["temperature_2m"],
        humidity=current["relative_humidity_2m"],
        wind_speed=current["wind_speed_10m"],
        wind_direction=current["wind_direction_10m"],
        weather_code=current["weather_code"],
        location_name=location_name,
        latitude=lat,
        longitude=lon,
    )


def get_cached_weather(
    lat: float, lon: float, location_name: str = "Unknown", ttl: int = 300
):
    """Fetch weather with Streamlit's cache_data decorator applied.

    Wraps get_current_weather in a dynamically created cached function so
    repeated calls with the same coordinates are served from cache.

    Note: Must be called within a running Streamlit application.

    Args:
        lat: Geographic latitude in decimal degrees (-90 to 90).
        lon: Geographic longitude in decimal degrees (-180 to 180).
        location_name: Human-readable name attached to the returned data.
            Defaults to "Unknown".
        ttl: Cache time-to-live in seconds. Defaults to 300.

    Returns:
        A WeatherData instance for the given coordinates.
    """
    import streamlit as st

    @st.cache_data(ttl=ttl)
    def _fetch_weather(lat: float, lon: float, location_name: str) -> WeatherData:
        return get_current_weather(lat, lon, location_name)

    return _fetch_weather(lat, lon, location_name)
