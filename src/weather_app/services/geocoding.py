"""City geocoding via the Open-Meteo Geocoding API."""

import requests
from typing import Optional

from src.weather_app.models.weather_data import GeocodingResult


class GeocodingError(Exception):
    """Raised when geocoding API fails."""

    pass


class NetworkError(Exception):
    """Raised when network connectivity fails."""

    pass


def search_city(city_name: str) -> Optional[GeocodingResult]:
    """Search for a city by name using the Open-Meteo Geocoding API.

    Args:
        city_name: The city name to search for. Must be non-empty after
            stripping whitespace.

    Returns:
        A GeocodingResult with the top match's coordinates and name, or
        None if no results were found.

    Raises:
        GeocodingError: If city_name is empty or blank.
        NetworkError: If the HTTP request fails due to a connectivity issue.
    """
    if not city_name or not city_name.strip():
        raise GeocodingError("City name cannot be empty")

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name.strip(), "count": 1, "language": "en", "format": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Network error while searching for city: {e}")

    data = response.json()

    if not data.get("results") or len(data["results"]) == 0:
        return None

    result = data["results"][0]
    return GeocodingResult(
        name=result["name"],
        latitude=result["latitude"],
        longitude=result["longitude"],
        country=result.get("country"),
    )
