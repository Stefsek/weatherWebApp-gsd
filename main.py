"""Streamlit weather application entry point.

Provides the main UI for searching cities and displaying current weather
conditions including temperature, humidity, wind speed, and an interactive map.

Typical usage example:

  streamlit run main.py
"""
import streamlit as st

from streamlit_folium import st_folium
import folium

from src.weather_app.models.weather_data import WeatherData
from src.weather_app.services.geocoding import search_city, GeocodingError, NetworkError
from src.weather_app.services.weather import get_current_weather, WeatherAPIError
from src.weather_app.utils.formatters import format_weather_code, format_wind_direction
from src.weather_app.utils.converters import format_temperature


def init_session_state() -> None:
    """Initialize session state variables."""
    if "temperature_unit" not in st.session_state:
        st.session_state["temperature_unit"] = "C"
    if "weather_data" not in st.session_state:
        st.session_state["weather_data"] = None
    if "error_message" not in st.session_state:
        st.session_state["error_message"] = None
    if "last_searched_city" not in st.session_state:
        st.session_state["last_searched_city"] = None


def handle_city_search(city: str) -> None:
    """Search for a city and fetch its current weather data.

    Geocodes the city name, then fetches weather data, storing results in
    Streamlit session state. Sets error_message on failure.

    Args:
        city: The city name to search for.
    """
    if not city or not city.strip():
        return

    if city == st.session_state.get("last_searched_city") and st.session_state.get(
        "weather_data"
    ):
        return

    st.session_state["error_message"] = None
    st.session_state["weather_data"] = None

    try:
        geocoding_result = search_city(city.strip())
        if geocoding_result is None:
            st.session_state["error_message"] = (
                f"City '{city}' not found. Please try a different city."
            )
            st.session_state["last_searched_city"] = city
            return

        weather = get_current_weather(
            lat=geocoding_result.latitude,
            lon=geocoding_result.longitude,
            location_name=geocoding_result.name,
        )
        st.session_state["weather_data"] = weather
        st.session_state["last_searched_city"] = city

    except GeocodingError as e:
        st.session_state["error_message"] = f"Geocoding error: {str(e)}"
        st.session_state["last_searched_city"] = city
    except WeatherAPIError as e:
        st.session_state["error_message"] = f"Weather service error: {str(e)}"
        st.session_state["last_searched_city"] = city
    except NetworkError as e:
        st.session_state["error_message"] = (
            f"Network error: {str(e)}. Please check your internet connection."
        )
        st.session_state["last_searched_city"] = city
    except Exception as e:
        st.session_state["error_message"] = f"An unexpected error occurred: {str(e)}"
        st.session_state["last_searched_city"] = city


def display_weather(weather: WeatherData) -> None:
    """Render weather data as styled HTML cards and an interactive map.

    Args:
        weather: The WeatherData object containing current conditions.
    """
    unit = st.session_state["temperature_unit"]

    # Main weather card - City, Temp, Condition
    st.markdown(
        f"""
    <div style="background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 1.5rem; 
                margin: 1rem 0; text-align: center; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">
        <div style="font-size: 1rem; color: #e0e0e0; margin-bottom: 0.5rem;">{weather.location_name}</div>
        <div style="font-size: 2rem; font-weight: bold; color: #f9fafb; margin: 0.5rem 0;">{format_temperature(weather.temperature_c, unit)}</div>
        <div style="font-size: 1rem; color: #00d4ff;">{format_weather_code(weather.weather_code)}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Three metric cards: Humidity | Wind | Direction
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-label">Humidity</div>
            <div class="metric-value">{weather.humidity:.0f}%</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-label">Wind</div>
            <div class="metric-value">{weather.wind_speed:.1f} km/h</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-label">Direction</div>
            <div class="metric-value">{format_wind_direction(weather.wind_direction)}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Map below metrics
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    display_map(weather.latitude, weather.longitude, weather.location_name)

    # Footer
    st.markdown(
        """
    <div style="text-align: center; color: #6b7280; font-size: 0.75rem; margin-top: 1rem;">
        Open-Meteo API
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_map(latitude: float, longitude: float, location_name: str) -> None:
    """Render a Folium map centered on the given coordinates.

    Args:
        latitude: Geographic latitude of the location.
        longitude: Geographic longitude of the location.
        location_name: Display name used as the map marker popup label.
    """
    # Create map centered on location
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=10,
        tiles="CartoDB dark_matter",
    )

    # Add circle marker
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=10,
        color="#00d4ff",
        fill=True,
        fillColor="#00d4ff",
        fillOpacity=0.7,
        popup=location_name,
    ).add_to(m)

    m.get_root().html.add_child(
        folium.Element("<style>.leaflet-control-attribution{display:none!important}</style>")
    )

    st_folium(m, use_container_width=True, height=250)


def main() -> None:
    """Main application entry point."""
    # CSS for styling
    st.markdown(
        """
    <style>
    /* App gradient background */
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #12121a 100%) !important;
        min-height: 100vh;
    }

    /* Transparent header */
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Container padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1a24, #1e1e2a);
        border: 1px solid #2a2a3a;
        border-radius: 8px;
        padding: 0.875rem 0.5rem;
        text-align: center;
    }
    .metric-label {
        color: #9ca3af;
        font-size: 0.75rem;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-value {
        color: #f9fafb;
        font-size: 1.05rem;
        font-weight: 600;
    }

    /* C/F toggle - dark container */
    [data-testid="stSegmentedControl"] > div {
        background: #0e0e16 !important;
        border: 1px solid #2a2a3a !important;
        border-radius: 8px !important;
        padding: 3px !important;
    }

    /* C/F toggle - active option: cyan border outline */
    [data-testid="stSegmentedControl"] label:has(input:checked) {
        border: 1.5px solid #00d4ff !important;
        border-radius: 6px !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* C/F toggle - inactive option */
    [data-testid="stSegmentedControl"] label:not(:has(input:checked)) {
        border: 1.5px solid transparent !important;
        border-radius: 6px !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    container = st.container()
    with container:
        # Title with cloud icon
        st.markdown(
            """
        <h1 style='text-align: center; font-size: 1.5rem; margin-bottom: 1rem;'>
            <span style='background: linear-gradient(to right, #00d4ff, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                ☁️ Weather App
            </span>
        </h1>
        """,
            unsafe_allow_html=True,
        )

        init_session_state()

        # Search and temperature unit inline
        search_col, unit_col = st.columns([4, 1])
        with search_col:
            city = st.text_input(
                "Search city",
                placeholder="Enter city name...",
                key="city_input",
                label_visibility="collapsed",
            )
        with unit_col:
            unit = st.segmented_control(
                "Unit",
                options=["C", "F"],
                default=st.session_state["temperature_unit"],
                key="unit_selector",
                label_visibility="collapsed",
            )
        st.session_state["temperature_unit"] = unit

        if city:
            handle_city_search(city)

        if st.session_state.get("error_message"):
            st.error(st.session_state["error_message"])

        if st.session_state.get("weather_data"):
            display_weather(st.session_state["weather_data"])


if __name__ == "__main__":
    main()
